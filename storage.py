from uuid import UUID
from typing import Optional
from datetime import date


trainers: dict[UUID, dict] = {}
clients: dict[UUID, dict] = {}


def get_all_trainers() -> list[dict]:
    return list(trainers.values())


def get_trainer_by_id(trainer_id: UUID) -> Optional[dict]:
    return trainers.get(trainer_id)


def create_trainer(trainer: dict) -> dict:
    trainers[trainer["id"]] = trainer
    return trainer


def update_trainer(trainer_id: UUID, updates: dict) -> Optional[dict]:
    if trainer_id not in trainers:
        return None
    trainers[trainer_id].update(updates)
    return trainers[trainer_id]


def get_all_clients() -> list[dict]:
    return list(clients.values())


def get_client_by_id(client_id: UUID) -> Optional[dict]:
    return clients.get(client_id)


def create_client(client: dict) -> dict:
    clients[client["id"]] = client
    return client


def update_client(client_id: UUID, updates: dict) -> Optional[dict]:
    if client_id not in clients:
        return None
    clients[client_id].update(updates)
    return clients[client_id]


def get_clients_by_trainer(trainer_id: UUID) -> list[dict]:
    return [c for c in clients.values() if c.get("trainer_id") == trainer_id]
