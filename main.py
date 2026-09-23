import json
import os
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any

from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

from database import Base, engine, get_db
from models import Basket

class ForceHTTPSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request.scope["scheme"] = "https"
        response = await call_next(request)
        return response

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        Base.metadata.create_all(bind=engine)
        print("Таблицы успешно проверены/созданы в базе данных.")
    except Exception as e:
        print(f"КРИТИЧЕСКАЯ ОШИБКА ПРИ СОЗДАНИИ ТАБЛИЦ: {e}")
    yield

app = FastAPI(lifespan=lifespan)
if os.getenv("ENV") == "production":
    app.add_middleware(ForceHTTPSMiddleware)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/send_goods")
async def send_goods(data: list[Any], x_file_name: str = Header(None)):
    if not x_file_name:
        raise HTTPException(status_code=400, detail="Название файла обязателен")

    filename = os.path.basename(x_file_name)
    if not filename.endswith(".json"):
        filename += ".json"

    file_path = os.path.join(UPLOAD_DIR, filename)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при записи файла: {str(e)}")

    return {
        "status": "success",
        "filename": filename
    }


@app.get("/get_goods/{filename}")
async def get_goods(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Файл не найден")

    if not filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="Можно запрашивать только JSON файлы")

    return FileResponse(path=file_path, media_type='application/json', filename=filename)


@app.post("/save_basket")
async def save_basket(payload: dict[str, Any], db: Session = Depends(get_db)):
    """
    Принимает JSON-тело запроса, парсит метаданные и сохраняет структуру в таблицу basket.
    """
    uuid_1c = payload.get("uuid1C")
    doc_date_str = payload.get("docDate")
    items = payload.get("items")

    if not uuid_1c:
        raise HTTPException(status_code=400, detail="Поле 'uuid1C' обязательно для заполнения")

    if items is None:
        raise HTTPException(status_code=400, detail="Товары обязательно для заполнения")

    doc_date = None
    if doc_date_str:
        try:
            doc_date = datetime.strptime(doc_date_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Неверный формат даты 'docDate'. Используйте YYYY-MM-DD HH:MM:SS"
            )

    try:
        # Передаём объект `items` (list/dict) напрямую в модель.
        # SQLAlchemy сам преобразователь его в JSON при сохранении в базу.
        db_basket = Basket(
            id_doc=str(uuid_1c),
            goods_json=items,  # Больше не нужен json.dumps()
            doc_date=doc_date
        )

        db.add(db_basket)
        db.commit()
        db.refresh(db_basket)

        return {
            "status": "success",
            "message": "Данные успешно сохранены",
            "basket_id": db_basket.id
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при работе с базой данных: {str(e)}")

from admin import init_admin
init_admin(app)