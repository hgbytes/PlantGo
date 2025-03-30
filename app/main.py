from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import torch
from PIL import Image
import io
import os
from models.model_utils import load_model, predict_disease
import pandas as pd

app = FastAPI(
    title="Plant Disease Detection API",
    description="API for detecting plant diseases using deep learning",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models/plant_disease_model_1.pt')
try:
    model = load_model(MODEL_PATH)
except Exception as e:
    print(f"Error loading model: {str(e)}")
    model = None

# Load disease information
try:
    disease_info = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data/disease_info.csv'))
    supplement_info = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data/supplement_info.csv'))
except Exception as e:
    print(f"Error loading data files: {str(e)}")
    disease_info = None
    supplement_info = None

@app.get("/")
async def root():
    return {"message": "Welcome to Plant Disease Detection API"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # Read and process the image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        
        # Save the image temporarily
        temp_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static/uploads', file.filename)
        os.makedirs(os.path.dirname(temp_path), exist_ok=True)
        image.save(temp_path)
        
        # Make prediction
        prediction_idx, disease_name = predict_disease(model, temp_path)
        
        # Get disease information
        disease_data = None
        if disease_info is not None:
            disease_data = disease_info[disease_info['disease_name'] == disease_name].to_dict('records')[0]
        
        # Get supplement information
        supplement_data = None
        if supplement_info is not None:
            supplement_data = supplement_info[supplement_info['index'] == prediction_idx].to_dict('records')
        
        # Clean up
        os.remove(temp_path)
        
        return {
            "disease_name": disease_name,
            "disease_info": disease_data,
            "supplements": supplement_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "data_loaded": disease_info is not None and supplement_info is not None
    } 