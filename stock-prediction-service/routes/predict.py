from flask import Blueprint, request, jsonify
import yfinance as yf
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import load_model
from keras.models import load_model
from keras.losses import MeanSquaredError
import joblib
import os

predict_blueprint = Blueprint('predict', __name__)

# Load the trained model & scaler
MODEL_PATH = "models/lstm_model.h5"
SCALER_PATH = "models/scaler.pkl"


# Explicitly register MSE before loading the model
custom_objects = {"mse": MeanSquaredError()}


if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
    # model = load_model(MODEL_PATH)
    model = load_model(MODEL_PATH, custom_objects=custom_objects) 
    scaler = joblib.load(SCALER_PATH)
else:
    model, scaler = None, None

@predict_blueprint.route('/stock', methods=['POST'])
def predict_stock():
    if not model or not scaler:
        return jsonify({"error": "Model not trained yet. Please train the model first."}), 500

    data = request.get_json()
    stock_symbol = data.get("symbol")

    if not stock_symbol:
        return jsonify({"error": "Stock symbol is required"}), 400

    # Fetch recent stock data
    stock_data = yf.download(stock_symbol, period="60d", interval="1d")

    if stock_data.empty:
        return jsonify({"error": "Invalid stock symbol or no data available"}), 400

    # Prepare input for prediction
    stock_data["Close"] = stock_data["Close"].fillna(method="ffill")
    last_50_days = stock_data["Close"].values[-50:].reshape(-1, 1)
    last_50_days_scaled = scaler.transform(last_50_days)

    # Reshape for LSTM
    X_test = np.array([last_50_days_scaled])
    predicted_price_scaled = model.predict(X_test)
    predicted_price = scaler.inverse_transform(predicted_price_scaled)[0][0]

    return jsonify({
        "symbol": stock_symbol,
        "predicted_price": round(float(predicted_price), 2)
    })