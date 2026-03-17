from fastapi import FastAPI
from pydantic import BaseModel, Field,computed_field
from typing import Annotated, Literal
import joblib
import pandas as pd
import numpy as np

#  Load the trained model AND the columns at the top
model = joblib.load('xgb_model.pkl')
model_columns = joblib.load('model_columns.pkl')

# Define the FastAPI app
app = FastAPI()

# Define the input data model
class CarData(BaseModel):
    brand: Annotated[str, Field(...,description="Car brand (e.g., Toyota, Ford)")]
    model_year: Annotated[int , Field(...,description="Model Year (e.g.,2012,2018)")]
    milage: Annotated[int, Field(...,description="Mileage (e.g., 50000, 75000)",gt=0)]
    fuel_type: Annotated[str, Field(...,description="Fuel Type (e.g., Gas, Diesel)")]
    transmission: Annotated[str, Field(...,description="Transmission (e.g., Manual, Automatic)")]
    horsepower: Annotated[float, Field(...,description="Horsepower (e.g., 200, 300)",gt=0)]
    liters: Annotated[float, Field(...,description="Liters (e.g., 2.0, 3.5)",gt=0)]
    accident: Annotated[str, Field(...,description="Accident (e.g., Yes, No)")]
    clean_title: Annotated[str, Field(...,description="Clean Title (e.g., Yes, No)")]
@app.get("/")
def home():
    return {"message": "Welcome to the Used Car Price Prediction System! Use the /predict endpoint to get a price estimate."}

@app.get("/health")
def health_check():
    return {"status": "OK",
            "message": "The model is loaded and the API is running smoothly!"
            }
            # Model Version

@app.post("/predict")
def predict_price(item: CarData):
    # Convert the Pydantic object to a dictionary
    input_dict = {
        'milage': item.milage,
        'hp': item.horsepower,
        'liters': item.liters,
        'car_age': 2026 - item.model_year,
        'accident': 1 if item.accident.lower() == "yes" else 0,
        'clean_title': 1 if item.clean_title.lower() == "yes" else 0,
        'brand': item.brand,
        'fuel_type': item.fuel_type,
        'transmission': item.transmission
    }

    # 2. Convert to DataFrame
    df = pd.DataFrame([input_dict])

    # 3. One-Hot Encoding
    df_encoded = pd.get_dummies(df)

    # 4. ALIGNMENT (The 87-Column Bridge)
    # Ensure model_columns is loaded globally!
    df_final = df_encoded.reindex(columns=model_columns, fill_value=0)

    # 5. Prediction
    prediction = model.predict(df_final)
    
    # Reverse Log Transform 
    
    final_price = np.expm1(prediction[0])
    # final_price = float(prediction[0])

    # 6. RETURN (This must be the last line of the function)
    return {
        "status": "Success",
        "predicted_price": f"${round(float(final_price), 2)}"
    }