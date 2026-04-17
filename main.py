import os

from fastapi import FastAPI, Request, Header

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