from fastapi import APIRouter, HTTPException
from uuid import uuid4, UUID
from app.models import (
    TrainerCreate, TrainerUpdate, TrainerStatusUpdate,
    TrainerResponse, TrainerDetailResponse
)
from app import storage

router = APIRouter(prefix="/api/trainers", tags=["Trainers"])


def _to_response(t: dict) -> TrainerResponse:
    return TrainerResponse(**t)


@router.post("", response_model=TrainerResponse, status_code=201)
def create_trainer(body: TrainerCreate):
    trainer = {
        "id": uuid4(),
        "surname": body.surname,
        "name": body.name,
        "patronymic": body.patronymic,
        "phone": body.phone,
        "status": body.status,
    }
    storage.create_trainer(trainer)
    return _to_response(trainer)


@router.put("/{trainer_id}", response_model=TrainerResponse)
def update_trainer(trainer_id: UUID, body: TrainerUpdate):
    existing = storage.get_trainer_by_id(trainer_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Тренер не найден")

    updates = body.model_dump(exclude_none=True)
    updated = storage.update_trainer(trainer_id, updates)
    return _to_response(updated)


@router.patch("/{trainer_id}/status", response_model=TrainerResponse)
def update_trainer_status(trainer_id: UUID, body: TrainerStatusUpdate):
    existing = storage.get_trainer_by_id(trainer_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Тренер не найден")

    updated = storage.update_trainer(trainer_id, {"status": body.status})
    return _to_response(updated)


@router.get("", response_model=list[TrainerResponse])
def get_all_trainers():
    return [_to_response(t) for t in storage.get_all_trainers()]


@router.get("/{trainer_id}/detail", response_model=TrainerDetailResponse)
def get_trainer_detail(trainer_id: UUID):
    trainer = storage.get_trainer_by_id(trainer_id)
    if not trainer:
        raise HTTPException(status_code=404, detail="Тренер не найден")

    clients = storage.get_clients_by_trainer(trainer_id)
    return TrainerDetailResponse(**trainer, clients=clients)
