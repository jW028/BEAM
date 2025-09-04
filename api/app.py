from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import os
from typing import Optional

app = FastAPI(
    title="Burnout Prediction API",
    description="API for predicting employee burnout risk",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and scaler on startup
MODEL_PATH = "../models/burnout_prediction_model.pkl"
LOWER_MODEL_PATH = "../models/lower_quantile_model.pkl"
UPPER_MODEL_PATH = "../models/upper_quantile_model.pkl"
SCALER_PATH = "../models/feature_scaler.pkl"

try:
    model = joblib.load(MODEL_PATH)
    lower_model = joblib.load(LOWER_MODEL_PATH)
    upper_model = joblib.load(UPPER_MODEL_PATH)
    print(f"Models loaded successfully from models directory")
except Exception as e:
    print(f"Error loading models: {e}")
    model = None

try:
    scaler = joblib.load(SCALER_PATH)
    print(f"Scaler loaded successfully from {SCALER_PATH}")
except Exception as e:
    print(f"Error loading scaler: {e}")
    scaler = None

class EmployeeData(BaseModel):
    designation: int
    resource_allocation: float
    mental_fatigue: float
    is_male: int  # 0 or 1
    is_service: int  # 0 or 1
    wfh_available: int  # 0 or 1

class PredictionResponse(BaseModel):
    predicted_burn_rate: float
    risk_category: str
    confidence_score: Optional[float] = None

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    scaler_loaded: bool

def categorize_burnout_risk(burn_rate: float) -> str:
    """Categorize burnout risk based on burn rate"""
    if burn_rate <= 0.3:
        return 'Low Risk'
    elif burn_rate <= 0.6:
        return 'Medium Risk'
    else:
        return 'High Risk'

def validate_input(employee: EmployeeData) -> None:
    """Validate input parameters"""
    if employee.designation < 0 or employee.designation > 5:
        raise HTTPException(status_code=400, detail="Designation must be between 0 and 5")
    
    if employee.resource_allocation < 0 or employee.resource_allocation > 10:
        raise HTTPException(status_code=400, detail="Resource allocation must be between 0 and 10")
    
    if employee.mental_fatigue < 0 or employee.mental_fatigue > 10:
        raise HTTPException(status_code=400, detail="Mental fatigue must be between 0 and 10")
    
    if employee.is_male not in [0, 1]:
        raise HTTPException(status_code=400, detail="is_male must be 0 or 1")
    
    if employee.is_service not in [0, 1]:
        raise HTTPException(status_code=400, detail="is_service must be 0 or 1")
    
    if employee.wfh_available not in [0, 1]:
        raise HTTPException(status_code=400, detail="wfh_available must be 0 or 1")

@app.get("/", summary="Root endpoint")
async def root():
    return {"message": "Burnout Prediction API", "version": "1.0.0"}

@app.get("/health", response_model=HealthResponse, summary="Health check")
async def health_check():
    """Check if the API and model are working properly"""
    return HealthResponse(
        status="healthy" if (model is not None and scaler is not None) else "unhealthy",
        model_loaded=model is not None,
        scaler_loaded=scaler is not None
    )

@app.post("/predict", response_model=PredictionResponse, summary="Predict burnout risk")
async def predict_burnout(employee: EmployeeData):
    """
    Predict burnout risk for an employee based on their characteristics.
    
    - **designation**: Job level (0-5)
    - **resource_allocation**: Resource allocation score (0-10)
    - **mental_fatigue**: Mental fatigue score (0-10)
    - **is_male**: Gender (0=Female, 1=Male)
    - **is_service**: Company type (0=Product, 1=Service)
    - **wfh_available**: Work from home available (0=No, 1=Yes)
    """
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    if scaler is None:
        raise HTTPException(status_code=500, detail="Scaler not loaded")
    
    try:
        # Validate input
        validate_input(employee)
        
        # Convert to DataFrame matching training format
        data = pd.DataFrame({
            'is_male': [employee.is_male],
            'is_service': [employee.is_service],
            'wfh_available': [employee.wfh_available],
            'Designation': [employee.designation],
            'Resource Allocation': [employee.resource_allocation],
            'Mental Fatigue Score': [employee.mental_fatigue]
        })
        
        numeric_cols = ['Resource Allocation', 'Mental Fatigue Score']
        data[numeric_cols] = scaler.transform(data[numeric_cols])
        
        # Make prediction
        prediction = model.predict(data)[0]
        
        # Ensure prediction is in valid range [0, 1]
        prediction = np.clip(prediction, 0, 1)
        
        risk = categorize_burnout_risk(prediction)
        
        lower_bound = lower_model.predict(data)[0]
        upper_bound = upper_model.predict(data)[0]
        # Use absolute value to prevent negative width if predictions cross
        interval_width = abs(upper_bound - lower_bound)

        # Confidence is inversely proportional to the prediction interval width
        # Lower interval width = higher confidence
        confidence = max(0.0, min(1.0, 1.0 - interval_width))
        
        
        return PredictionResponse(
            predicted_burn_rate=float(prediction),
            risk_category=risk,
            confidence_score=float(confidence)
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

@app.post("/predict/batch", summary="Batch predict burnout risk")
async def predict_burnout_batch(employees: list[EmployeeData]):
    """
    Predict burnout risk for multiple employees at once.
    Limited to 100 employees per request.
    """
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    if scaler is None:
        raise HTTPException(status_code=500, detail="Scaler not loaded")
    
    if len(employees) > 100:
        raise HTTPException(status_code=400, detail="Maximum 100 employees per batch request")
    
    try:
        # Create a single DataFrame for efficiency
        df = pd.DataFrame([emp.dict() for emp in employees])
        
        # Validate all inputs at once (optional, but good practice)
        for _, row in df.iterrows():
            validate_input(EmployeeData(**row))

        # Convert to training format column names
        df_training = pd.DataFrame({
            'is_male': df['is_male'],
            'is_service': df['is_service'], 
            'wfh_available': df['wfh_available'],
            'Designation': df['designation'],
            'Resource Allocation': df['resource_allocation'],
            'Mental Fatigue Score': df['mental_fatigue']
        })
        
        # Apply scaling to the entire batch
        numeric_cols = ['Resource Allocation', 'Mental Fatigue Score']
        df_training[numeric_cols] = scaler.transform(df_training[numeric_cols])
        
        # Get all predictions at once
        predictions = np.clip(model.predict(df_training), 0, 1)
        lower_bounds = lower_model.predict(df_training)
        upper_bounds = upper_model.predict(df_training)
        
        # Calculate all confidence scores
        interval_widths = np.abs(upper_bounds - lower_bounds)
        confidences = np.maximum(0.0, 1.0 - interval_widths)
        
        # Build response
        response = [
            PredictionResponse(
                predicted_burn_rate=float(pred),
                risk_category=categorize_burnout_risk(pred),
                confidence_score=float(conf)
            ) for pred, conf in zip(predictions, confidences)
        ]
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Batch prediction error: {str(e)}")

@app.get("/model/info", summary="Get model information")
async def model_info():
    """Get information about the loaded model"""
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    return {
        "model_type": str(type(model).__name__),
        "feature_count": model.n_features_in_ if hasattr(model, 'n_features_in_') else "unknown",
        "model_path": MODEL_PATH
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
