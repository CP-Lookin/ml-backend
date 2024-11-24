from fastapi import FastAPI
from fastapi import UploadFile, File
from PIL import Image
import numpy as np
import tensorflow as tf

app = FastAPI()

model = tf.keras.models.load_model('./model/tl_vgg16_2.h5')

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/predict/", response_model=dict, status_code=200)
async def predict(file: UploadFile = File(...)):
    image = Image.open(file.file)
    image = image.resize((224, 224))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
        
    predictions = model.predict(image)
    class_names = ['oval', 'round', 'square']
    predicted_class = class_names[np.argmax(predictions)]
        
    return {"predicted_class": predicted_class}