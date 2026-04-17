import os

from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import FileResponse

app = FastAPI()

UPLOAD_DIR = "temp_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {"Hello": "Hello my friend"}

@app.post("/upload-1c")
async def upload_from_1c(request: Request, x_file_name: str = Header(None)):
    body_content = await request.body()

    filename = x_file_name
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        buffer.write(body_content)

    return {"status": "succes", "filename": filename, "size": len(body_content)}


@app.get("/get-json/{filename}")
async def get_json_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)

    # Проверяем, существует ли файл и является ли он JSON
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Файл не найден")

    if not filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="Можно запрашивать только JSON файлы")

    return FileResponse(path=file_path, media_type='application/json', filename=filename)