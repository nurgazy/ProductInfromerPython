import os

from fastapi import FastAPI, UploadFile, File

app = FastAPI()

UPLOAD_DIR = "temp_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {"Hello": "Hello my friend"}

@app.post("/upload-1c")
async def upload_from_1c(file: UploadFile = File(...)):
    file_id = f"{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, file_id)

    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    return {"status": "saved", "file_id": file_id}