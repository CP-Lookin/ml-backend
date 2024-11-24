from fastapi import FastAPI, UploadFile, File, HTTPException
from PIL import Image, UnidentifiedImageError
import numpy as np
import tensorflow as tf
import logging

app = FastAPI()

# Load the model 
try:
    model = tf.keras.models.load_model('./model/tl_vgg16_2.h5')
except Exception as e:
    logging.error(f"Error loading model: {e}")
    raise RuntimeError("Failed to load model")

class_names = ['oval', 'round', 'square']

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/predict/", response_model=dict, status_code=200)
async def predict(file: UploadFile = File(...)):
    try:
        image = Image.open(file.file)
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Invalid image file")
    except Exception as e:
        logging.error(f"Error opening image: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    try:
        image = image.resize((224, 224))
        image = np.array(image) / 255.0
        image = np.expand_dims(image, axis=0)
        
        predictions = model.predict(image)
        predicted_class = class_names[np.argmax(predictions)]
    except Exception as e:
        logging.error(f"Error processing image: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
        
    return {"predicted_class": predicted_class}