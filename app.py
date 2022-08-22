import base64
from cmath import phase
from html.parser import HTMLParser
from fastapi import FastAPI, File, UploadFile, Request
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


import pytesseract as ocr
import numpy as np
import cv2
from PIL import Image


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


def filter(image: File):
    # load the example image and convert it to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # apply thresholding to preprocess the image
    _, gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # apply median blurring to remove any blurring
    gray = cv2.medianBlur(gray, 3)
    return gray


def base64_encode(image, imageFormat):
    _, img_res = cv2.imencode(imageFormat, image)
    encoded_image_base64 = base64.b64encode(img_res.tobytes()).decode('utf-8')
    
    return encoded_image_base64


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("layout.html", {"request": request})


@app.post("/")
async def create_file(request: Request, file: UploadFile = File(...)):

    contents = file.file.read()
    contents = np.fromstring(contents, np.uint8)

    # https://nanonets.com/blog/ocr-with-tesseract/

    image = cv2.imdecode(contents, cv2.IMREAD_COLOR)

    gray = filter(image)

    phrase = ocr.image_to_string(gray, lang='por')
    phrase = phrase.split("\n")
    imageFormat = "."+file.filename.split(".")[-1]
    encoded_image_base64 = base64_encode(image=image, imageFormat=imageFormat)

    # phrase=phrase.replace("\n", "</br>")
    # print(phrase)

    return templates.TemplateResponse("layout.html",
                                      {
                                          "request": request,
                                          "phrase": phrase,
                                          "format":imageFormat,
                                          "img_input": encoded_image_base64
                                      })


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}

if __name__ == "__main__":

    app_str = 'app:app'
    uvicorn.run(app_str, reload=True, host='0.0.0.0')
