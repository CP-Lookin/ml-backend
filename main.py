from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, UnidentifiedImageError
import numpy as np
import tensorflow as tf
import logging

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load the model 
try:
    face_shape_model = tf.keras.models.load_model('./model/tl_vgg16_2.h5')
    gender_model = tf.keras.models.load_model('./model/gender_tl_vgg16.h5')
except Exception as e:
    logging.error(f"Error loading model: {e}")
    raise RuntimeError("Failed to load model")

class_names = ['oval', 'round', 'square']
gender_class_names = ['female', 'male']

@app.get("/")
async def root():
    return {"message": "Hello World from Lookin App!"}

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
        
        face_shape_predictions = face_shape_model.predict(image)
        gender_predictions = gender_model.predict(image)
        
        predicted_face_shape = class_names[np.argmax(face_shape_predictions)]
        if gender_predictions[0] > 0.5:
            predicted_gender = "Male"
        else:
            predicted_gender = "Female"
    except Exception as e:
        logging.error(f"Error processing image: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
        
    return {
        "code" : 200,
        "message": "Prediction successful",
        "data": {
            "predicted_face_shape": predicted_face_shape,
            "predicted_gender": predicted_gender
        }
    }