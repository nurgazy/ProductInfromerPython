import json
import os
from typing import Dict, Any

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import FileResponse

app = FastAPI()

UPLOAD_DIR = "temp_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {"Hello": "Hello my friend"}

@app.post("/send_goods")
async def send_goods(data: Dict[Any, Any], x_file_name: str = Header(None)):
    if not x_file_name:
        raise HTTPException(status_code=400, detail="Название файла обязателен")

    filename = os.path.basename(x_file_name)
    if not filename.endswith(".json"):
        filename += ".json"

    file_path = os.path.join(UPLOAD_DIR, filename)

    # Сохраняем данные как JSON-файл
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