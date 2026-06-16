from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from uuid import UUID
from datetime import date
from enum import Enum
import re


class TrainerStatus(str, Enum):
    WORKING = "WORKING"
    ON_LEAVE = "ON_LEAVE"
    NOT_WORKING = "NOT_WORKING"


class TrainerCreate(BaseModel):
    surname: str
    name: str
    patronymic: Optional[str] = None
    phone: str
    status: TrainerStatus = TrainerStatus.WORKING

    @field_validator("surname", "name")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Поле не может быть пустым")
        return v.strip()

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        cleaned = re.sub(r"[\s\-\(\)\+]", "", v)
        if not cleaned.isdigit() or not (7 <= len(cleaned) <= 15):
            raise ValueError("Некорректный номер телефона")
        return v


class TrainerUpdate(BaseModel):
    surname: Optional[str] = None
    name: Optional[str] = None
    patronymic: Optional[str] = None
    phone: Optional[str] = None

    @field_validator("surname", "name")
    @classmethod
    def not_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("Поле не может быть пустым")
        return v.strip() if v else v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        cleaned = re.sub(r"[\s\-\(\)\+]", "", v)
        if not cleaned.isdigit() or not (7 <= len(cleaned) <= 15):
            raise ValueError("Некорректный номер телефона")
        return v


class TrainerStatusUpdate(BaseModel):
    status: TrainerStatus


class TrainerResponse(BaseModel):
    id: UUID
    surname: str
    name: str
    patronymic: Optional[str]
    phone: str
    status: TrainerStatus


class TrainerShort(BaseModel):
    id: UUID
    name: str
    surname: str
    status: TrainerStatus


class ClientCreate(BaseModel):
    surname: str
    name: str
    patronymic: Optional[str] = None
    birthday: date
    phone: str
    email: str
    trainer_id: Optional[UUID] = None

    @field_validator("surname", "name")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Поле не может быть пустым")
        return v.strip()

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        cleaned = re.sub(r"[\s\-\(\)\+]", "", v)
        if not cleaned.isdigit() or not (7 <= len(cleaned) <= 15):
            raise ValueError("Некорректный номер телефона")
        return v

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(pattern, v):
            raise ValueError("Некорректный email адрес")
        return v.lower()

    @field_validator("birthday")
    @classmethod
    def validate_birthday(cls, v: date) -> date:
        if v >= date.today():
            raise ValueError("Дата рождения должна быть в прошлом")
        return v


class ClientUpdate(BaseModel):
    surname: Optional[str] = None
    name: Optional[str] = None
    patronymic: Optional[str] = None
    birthday: Optional[date] = None
    phone: Optional[str] = None
    email: Optional[str] = None

    @field_validator("surname", "name")
    @classmethod
    def not_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("Поле не может быть пустым")
        return v.strip() if v else v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        cleaned = re.sub(r"[\s\-\(\)\+]", "", v)
        if not cleaned.isdigit() or not (7 <= len(cleaned) <= 15):
            raise ValueError("Некорректный номер телефона")
        return v

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(pattern, v):
            raise ValueError("Некорректный email адрес")
        return v.lower()

    @field_validator("birthday")
    @classmethod
    def validate_birthday(cls, v: Optional[date]) -> Optional[date]:
        if v is not None and v >= date.today():
            raise ValueError("Дата рождения должна быть в прошлом")
        return v


class ClientStatusUpdate(BaseModel):
    is_active: bool


class ClientResponse(BaseModel):
    id: UUID
    surname: str
    name: str
    patronymic: Optional[str]
    birthday: date
    phone: str
    email: str
    is_active: bool
    trainer_id: Optional[UUID]


class ClientDetailResponse(BaseModel):
    id: UUID
    surname: str
    name: str
    patronymic: Optional[str]
    birthday: date
    phone: str
    email: str
    is_active: bool
    trainer: Optional[TrainerShort]


class TrainerDetailResponse(BaseModel):
    id: UUID
    surname: str
    name: str
    patronymic: Optional[str]
    phone: str
    status: TrainerStatus
    clients: list[ClientResponse]
