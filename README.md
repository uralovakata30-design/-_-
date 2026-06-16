# Fitness Center REST API

## Технологии

- **Python 3.11+**
- **FastAPI** — веб-фреймворк
- **Pydantic v2** — валидация данных
- **Uvicorn** — ASGI-сервер
- **Хранилище** — in-memory (dict в оперативной памяти)

## Запуск

```bash
pip install fastapi uvicorn
uvicorn main:app --reload
```

Документация Swagger: http://localhost:8000/docs

---

## API Endpoints

### Клиенты `/api/clients`

| Метод  | Путь                                      | Описание                          |
|--------|-------------------------------------------|-----------------------------------|
| POST   | `/api/clients`                            | Создать клиента                   |
| PUT    | `/api/clients/{id}`                       | Обновить данные клиента           |
| GET    | `/api/clients`                            | Список всех клиентов              |
| GET    | `/api/clients/{id}`                       | Краткая информация о клиенте     |
| GET    | `/api/clients/{id}/detail`                | Подробная информация с тренером   |
| PATCH  | `/api/clients/{id}/status`                | Активировать / деактивировать     |
| POST   | `/api/clients/{clientId}/trainer/{trainerId}` | Назначить тренера            |

### Тренеры `/api/trainers`

| Метод  | Путь                          | Описание                              |
|--------|-------------------------------|---------------------------------------|
| POST   | `/api/trainers`               | Создать тренера                       |
| PUT    | `/api/trainers/{id}`          | Обновить данные тренера               |
| PATCH  | `/api/trainers/{id}/status`   | Изменить статус тренера               |
| GET    | `/api/trainers`               | Список всех тренеров                  |
| GET    | `/api/trainers/{id}/detail`   | Подробная информация со списком клиентов |

---

## Модели данных

### Client
```json
{
  "surname": "Иванов",
  "name": "Иван",
  "patronymic": "Иванович",
  "birthday": "1990-05-15",
  "phone": "+79001234567",
  "email": "ivan@example.com",
  "trainer_id": null
}
```

### Trainer
```json
{
  "surname": "Петров",
  "name": "Алексей",
  "patronymic": "Сергеевич",
  "phone": "+79009876543",
  "status": "WORKING"
}
```

Статусы тренера: `WORKING` | `ON_LEAVE` | `NOT_WORKING`

---

## Коды ответов

| Код | Описание                     |
|-----|------------------------------|
| 201 | Ресурс успешно создан        |
| 200 | Успешный запрос              |
| 400 | Ошибка валидации             |
| 404 | Ресурс не найден             |

## Структура проекта

```
fitness_api/
├── main.py              # Точка входа, FastAPI app
├── app/
│   ├── models.py        # Pydantic-схемы (Request / Response)
│   ├── storage.py       # In-memory хранилище (заменяется на БД в части 2)
│   └── routers/
│       ├── clients.py   # Эндпоинты клиентов
│       └── trainers.py  # Эндпоинты тренеров
```
