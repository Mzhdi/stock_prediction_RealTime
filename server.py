import joblib
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from flask import Flask, request, jsonify


def predict_stock_trade_decision(model, today_features):
    # Predict whether it's a good day to open or close based on today's features
    prediction = model.predict([today_features])

    # Interpret the prediction
    if prediction[0] == 1:
        return "Open"  # Good day to open a position
    else:
        return "Close"  # Good day to close a position


# Initial model filename
model_filename = 'stock_prediction_model.pkl'


def train_and_save_model(stock_symbol, start_date, end_date, model_filename):
    # Fetch historical stock data from Yahoo Finance
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)

    # Create a DataFrame from the fetched data
    df = pd.DataFrame(stock_data)

    # Define a simple moving average (SMA) crossover strategy
    short_window = 20
    long_window = 50

    # Calculate the short-term SMA
    df['Short_MA'] = df['Close'].rolling(window=short_window).mean()

    # Calculate the long-term SMA
    df['Long_MA'] = df['Close'].rolling(window=long_window).mean()

    # Create labels based on the crossover strategy
    df['Label'] = 0  # Initialize all labels to 0 (Close deal)
    df['Label'][short_window:] = np.where(
        df['Short_MA'][short_window:] > df['Long_MA'][short_window:], 1, 0)

    # Drop rows with NaN values introduced by the rolling averages
    df.dropna(inplace=True)

    # Define your features and labels
    X = df[['Open', 'High', 'Low', 'Close', 'Volume', 'Short_MA', 'Long_MA']]
    y = df['Label']

    # Create and train a logistic regression model
    model = LogisticRegression()
    model.fit(X, y)

    # Save the trained model, overwriting the existing file if it exists
    joblib.dump(model, model_filename)
    print(f"Model saved as {model_filename}")


app = Flask(__name__)


@app.route('/train', methods=['POST'])
def train_model_endpoint():
    try:
        data = request.json
        stock_symbol = data['stock_symbol']
        start_date = data['start_date']
        end_date = data['end_date']

        # Train and save the model
        train_and_save_model(stock_symbol, start_date,
                             end_date, model_filename)

        return jsonify({'message': f"Model trained and saved as {model_filename}"})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/predict', methods=['POST'])
def predict_endpoint():
    try:
        data = request.json
        today_features = data['features']

        # Load the trained model
        model = joblib.load(model_filename)

        # Make a prediction using the loaded model
        prediction = predict_stock_trade_decision(model, today_features)

        # Return the prediction as JSON response
        response = {'prediction': prediction}
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
