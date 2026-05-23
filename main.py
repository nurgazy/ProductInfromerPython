import json
import os
from contextlib import asynccontextmanager
from typing import Any
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
from database import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        Base.metadata.create_all(bind=engine)
        print("Таблицы успешно проверены/созданы в базе данных.")
    except Exception as e:
        print(f"КРИТИЧЕСКАЯ ОШИБКА ПРИ СОЗДАНИИ ТАБЛИЦ: {e}")
    yield

app = FastAPI(lifespan=lifespan)

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