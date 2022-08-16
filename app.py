from fastapi import FastAPI, File, UploadFile
import uvicorn

app = FastAPI()

@app.get("/")
def home():
    return "Hello"

@app.post("/files/")
async def create_file(file: bytes = File()):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}

if __name__ == "__main__":

    app_str = 'app:app'
    uvicorn.run(app_str, reload=True, host='0.0.0.0')