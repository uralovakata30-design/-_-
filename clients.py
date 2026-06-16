from fastapi import APIRouter, HTTPException
from uuid import uuid4, UUID
from app.models import (
    ClientCreate, ClientUpdate, ClientStatusUpdate,
    ClientResponse, ClientDetailResponse, TrainerShort
)
from app import storage

router = APIRouter(prefix="/api/clients", tags=["Clients"])


def _to_response(c: dict) -> ClientResponse:
    return ClientResponse(**c)


@router.post("", response_model=ClientResponse, status_code=201)
def create_client(body: ClientCreate):
    if body.trainer_id is not None:
        trainer = storage.get_trainer_by_id(body.trainer_id)
        if not trainer:
            raise HTTPException(status_code=404, detail="Тренер не найден")

    client = {
        "id": uuid4(),
        "surname": body.surname,
        "name": body.name,
        "patronymic": body.patronymic,
        "birthday": body.birthday,
        "phone": body.phone,
        "email": body.email,
        "is_active": True,
        "trainer_id": body.trainer_id,
    }
    storage.create_client(client)
    return _to_response(client)


@router.put("/{client_id}", response_model=ClientResponse)
def update_client(client_id: UUID, body: ClientUpdate):
    existing = storage.get_client_by_id(client_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Клиент не найден")

    updates = body.model_dump(exclude_none=True)
    updated = storage.update_client(client_id, updates)
    return _to_response(updated)


@router.get("", response_model=list[ClientResponse])
def get_all_clients():
    return [_to_response(c) for c in storage.get_all_clients()]


@router.get("/{client_id}", response_model=ClientResponse)
def get_client(client_id: UUID):
    client = storage.get_client_by_id(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    return _to_response(client)


@router.get("/{client_id}/detail", response_model=ClientDetailResponse)
def get_client_detail(client_id: UUID):
    client = storage.get_client_by_id(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Клиент не найден")

    trainer_data = None
    if client.get("trainer_id"):
        trainer = storage.get_trainer_by_id(client["trainer_id"])
        if trainer:
            trainer_data = TrainerShort(
                id=trainer["id"],
                name=trainer["name"],
                surname=trainer["surname"],
                status=trainer["status"],
            )

    return ClientDetailResponse(
        id=client["id"],
        surname=client["surname"],
        name=client["name"],
        patronymic=client.get("patronymic"),
        birthday=client["birthday"],
        phone=client["phone"],
        email=client["email"],
        is_active=client["is_active"],
        trainer=trainer_data,
    )


@router.patch("/{client_id}/status", response_model=ClientResponse)
def update_client_status(client_id: UUID, body: ClientStatusUpdate):
    existing = storage.get_client_by_id(client_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Клиент не найден")

    updated = storage.update_client(client_id, {"is_active": body.is_active})
    return _to_response(updated)


@router.post("/{client_id}/trainer/{trainer_id}", response_model=ClientResponse)
def assign_trainer(client_id: UUID, trainer_id: UUID):
    client = storage.get_client_by_id(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Клиент не найден")

    trainer = storage.get_trainer_by_id(trainer_id)
    if not trainer:
        raise HTTPException(status_code=404, detail="Тренер не найден")

    updated = storage.update_client(client_id, {"trainer_id": trainer_id})
    return _to_response(updated)
