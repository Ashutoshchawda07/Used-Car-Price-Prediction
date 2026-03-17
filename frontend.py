import streamlit as st
import requests

API_URL = "http://localhost:8000/predict" 
# Streamlit App
st.title("Used Car Price Prediction")

st.markdown("Enter the details of the car to predict its price:")
brand = st.text_input("Car Brand (e.g., Toyota, Ford)")
model_year = st.number_input("Model Year (e.g., 2012, 2018)", min_value=1900, max_value=2026, step=1)
milage = st.number_input("Mileage (e.g., 50000, 75000)", min_value=0, step=1000)
fuel_type = st.selectbox("Fuel Type", ["Gas", "Diesel", "Electric", "Hybrid"])  
transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
horsepower = st.number_input("Horsepower (e.g., 200, 300)", min_value=0.0, step=0.1)
liters = st.number_input("Liters (e.g., 2.0, 3.5)", min_value=0.0, step=0.1)
accident = st.selectbox("Accident History", ["Yes", "No"])  
clean_title = st.selectbox("Clean Title", ["Yes", "No"])

if st.button("Predict Price"):
    input_data = {
        "brand": brand,
        "model_year": model_year,
        "milage": milage,
        "fuel_type": fuel_type,
        "transmission": transmission,
        "horsepower": horsepower,
        "liters": liters,
        "accident": accident,
        "clean_title": clean_title
    }
    
    response = requests.post(API_URL, json=input_data)
    
    if response.status_code == 200:
        result = response.json()
        st.success(f"Predicted Price: {result['predicted_price']}")
    else:
        st.error("Error in prediction. Please try again.")
        