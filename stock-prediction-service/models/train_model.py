import yfinance as yf
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from keras.optimizers import Adam
from keras.losses import MeanSquaredError
import joblib
import os


# # Define model path
# MODEL_PATH = "models/stock_prediction_model.h5"

# # Sample data (replace with actual dataset)
# X_train = np.random.rand(100, 10, 1)
# y_train = np.random.rand(100, 1)

# # Define the model
# model = Sequential([
#     LSTM(50, return_sequences=True, input_shape=(10, 1)),
#     LSTM(50),
#     Dense(1)
# ])

# # Explicitly define the loss function
# model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')

# # Train the model
# model.fit(X_train, y_train, epochs=10, batch_size=16, verbose=1)

# # Save the model explicitly with the loss function
# model.save(MODEL_PATH, include_optimizer=True)



def train_model(stock_symbol="AAPL", save_path="models/lstm_model.h5"):
    print(f"Training model for {stock_symbol}...")

    # Fetch historical stock data
    stock_data = yf.download(stock_symbol, period="2y", interval="1d")
    
    if stock_data.empty:
        print("No data found for the given stock symbol.")
        return None

    stock_data["Close"] = stock_data["Close"].fillna(method="ffill")

    # Prepare dataset
    data = stock_data["Close"].values.reshape(-1, 1)
    
    # Normalize the data
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler(feature_range=(0,1))
    data_scaled = scaler.fit_transform(data)

    # Save the scaler for future predictions
    joblib.dump(scaler, "models/scaler.pkl")

    # Create sequences for LSTM
    def create_sequences(data, seq_length=50):
        X, y = [], []
        for i in range(len(data) - seq_length):
            X.append(data[i : i + seq_length])
            y.append(data[i + seq_length])
        return np.array(X), np.array(y)

    X, y = create_sequences(data_scaled, seq_length=50)

    # Split into train & test sets
    split = int(0.8 * len(X))
    X_train, y_train = X[:split], y[:split]
    X_test, y_test = X[split:], y[split:]

    # Build the LSTM model
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(50,1)),
        LSTM(50, return_sequences=False),
        Dense(25, activation="relu"),
        Dense(1)
    ])
    
    # model.compile(optimizer="adam", loss="mse")
    model.compile(optimizer="adam", loss=MeanSquaredError(), metrics=["mae"])
    model.fit(X_train, y_train, batch_size=16, epochs=20, validation_data=(X_test, y_test))

    # Save the model
    os.makedirs("models", exist_ok=True)
    model.save(save_path)
    print(f"Model trained and saved to {save_path}")

# Train the model
if __name__ == "__main__":
    train_model()


# import numpy as np
# import pandas as pd
# import tensorflow as tf
# from keras.models import Sequential
# from keras.layers import LSTM, Dense
# from sklearn.preprocessing import MinMaxScaler
# import joblib
# import os

# # Paths
# DATA_PATH = "data/stock_prices.csv"  # Ensure this file is regularly updated
# MODEL_PATH = "models/stock_model.h5"
# SCALER_PATH = "models/scaler.pkl"

# # Load stock data
# df = pd.read_csv(DATA_PATH)
# df["Date"] = pd.to_datetime(df["Date"])
# df.set_index("Date", inplace=True)
# df = df[["Close"]]  # Use closing price for predictions

# # Normalize data
# scaler = MinMaxScaler()
# scaled_data = scaler.fit_transform(df)

# # Save the scaler
# joblib.dump(scaler, SCALER_PATH)

# # Prepare data for LSTM
# def create_sequences(data, seq_length):
#     X, y = [], []
#     for i in range(len(data) - seq_length):
#         X.append(data[i : i + seq_length])
#         y.append(data[i + seq_length])
#     return np.array(X), np.array(y)

# SEQ_LENGTH = 60  # Use 60 days of data to predict the next day
# X, y = create_sequences(scaled_data, SEQ_LENGTH)

# # Split into training and testing sets
# split = int(len(X) * 0.8)
# X_train, y_train = X[:split], y[:split]
# X_test, y_test = X[split:], y[split:]

# # Build LSTM Model
# model = Sequential([
#     LSTM(50, return_sequences=True, input_shape=(SEQ_LENGTH, 1)),
#     LSTM(50, return_sequences=False),
#     Dense(25),
#     Dense(1)
# ])

# model.compile(optimizer="adam", loss="mse")

# # Train the model
# model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=20, batch_size=16)

# # Save model
# model.save(MODEL_PATH)

# print("✅ Model training completed and saved!")
