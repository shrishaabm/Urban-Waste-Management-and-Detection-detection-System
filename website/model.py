from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse
import torch
from starlette.responses import FileResponse
from PIL import Image, ImageDraw
import io
from pydantic import BaseModel
import os
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import Geometry
from sqlalchemy.sql import func
from collections import defaultdict

import psycopg2

DATABASE_URL = "postgresql://postgresql:LIon1965@localhost/garbage_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


dbname = "garbage_db"
user = "postgres"
password = "LIon1965"
host = "localhost"
port = "5432"

try:
  conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
  print("Connection established successfully!")
except Exception as e:
  print(f"Connection error: {e}")
  exit()


cur = conn.cursor()

class Coordinates(BaseModel):
    lat: float
    lng: float

rqdata = defaultdict(lambda: {"image": None, "lat": None, "lng": None, "predict": None})

app = FastAPI()
# app.mount("/",StaticFiles(directory='templates',html=True),name='static')

@app.get("/")
async def read_index():
    return FileResponse('templates/index.html')

def load_model(weights_path):
    print(f"Loading model from {weights_path}")
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=weights_path, force_reload=True)
    return model

model = load_model('/Users/shrishaa/Garbage/yolov5/runs/train/yolo_bag_det/weights/best.pt')

def predict(model, image_bytes, save_path):
    try:
        print("Reading image bytes")
        img = Image.open(io.BytesIO(image_bytes))
        print("Image opened successfully")

        print("Running model prediction")
        results = model(img)
        print("Model prediction completed")

        bboxes = results.xyxy[0]
        print(f"Bounding boxes found: {bboxes}")

        mx = [max(list(bboxes), key=lambda _: _[4])]

        if mx:
            x1, y1, x2, y2, *_ = mx[0]
            draw = ImageDraw.Draw(img)
            draw.rectangle((x1, y1, x2, y2), fill=(255, 0, 0), width=2)

        img.save(f"{save_path}.png")

        return mx[0][4].item() > .7

    except Exception as e:
        print(f"Error during prediction: {e}")
        return False

@app.post("/upload-image")
async def upload_image(image: UploadFile, request: Request):
    try:
        print("Receiving uploaded image")
        image_bytes = await image.read()
        print(f"Image received: {len(image_bytes)} bytes")

        z = [int(os.path.splitext(f)[0]) for f in os.listdir("web_imgs") if os.path.splitext(f)[0].isnumeric()]
        if not z:
            z = [0]

        ip = request.client.host

        print(rqdata)

        save_path = f"web_imgs/{max(z)+1:04}"
        rqdata[ip]["image"] = save_path + ".png"

        # location = None
        # with open(f"{save_path}.txt") as wf:
        #     wf.write(str(location))
        


        prediction = predict(model, image_bytes,save_path=save_path)
        print(f"Prediction result: {prediction}")

        rqdata[ip]["predict"] = prediction

        image = rqdata[ip]["image"] or ""
        lat = rqdata[ip]["lat"] or 0.5
        lng = rqdata[ip]["lng"] or 0.5
        pred = rqdata[ip]["predict"] or "False"

        cur.execute(f"""INSERT INTO detection (image_path, latitude, longitude, detection) VALUES ('{image}', {lat}, {lng}, '{pred}')""")
        conn.commit()

        return JSONResponse(content={"prediction": prediction})
    except Exception as e:
        print(f"Error in /upload-image endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/receive-coordinates")
async def receive_coordinates(coordinates: Coordinates, request: Request):
    location_lat=coordinates.lat
    location_lng=coordinates.lng
    # with open('/Users/shrishaa/Garbage/website/coordinates/location.txt','a') as f:
    #     f.write(f'{coordinates}\n')

    ip = request.client.host
    rqdata[ip]["lat"] = location_lat
    rqdata[ip]["lng"] = location_lng
    
    z = [int(os.path.splitext(f)[0]) for f in os.listdir("/Users/shrishaa/Garbage/website/coordinates/") if os.path.splitext(f)[0].isnumeric()]
    if not z:
        z = [0]
    save_path = f"/Users/shrishaa/Garbage/website/coordinates/{max(z)+1:04}"
    with open(f"{save_path}.txt","w") as wf:
        wf.write(f'{location_lat},{location_lng}\n')


if __name__ == "__main__":
    try:
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)
    finally:
        conn.close()
