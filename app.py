import base64
from fastapi import FastAPI, File, UploadFile
import uvicorn

from fastapi.responses import StreamingResponse
from io import BytesIO

import pytesseract as ocr
import numpy as np
import cv2
from PIL import Image

app = FastAPI()

@app.get("/")
def home():
    return "Hello"

@app.post("/files/")
async def create_file(file: UploadFile = File(...)):  

    contents = file.file.read()
    contents = np.fromstring(contents, np.uint8)

    # https://nanonets.com/blog/ocr-with-tesseract/

    # load the example image and convert it to grayscale
    image = cv2.imdecode(contents, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # apply thresholding to preprocess the image
    _, gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    #apply median blurring to remove any blurring
    gray = cv2.medianBlur(gray, 3)
    # cv2.imwrite(file.filename, gray)
    phrase = ocr.image_to_string(gray, lang='por')

    format = "."+file.filename.split(".")[-1]

    img = cv2.resize(image, (64,64))
    _,img_res = cv2.imencode(format, img)
    encoded_image_string = base64.urlsafe_b64encode(img)

    return {
        "prase": phrase, 
        "img_input": encoded_image_string
        }
    # return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}

if __name__ == "__main__":

    app_str = 'app:app'
    uvicorn.run(app_str, reload=True, host='0.0.0.0')