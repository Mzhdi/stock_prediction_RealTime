from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# Load the saved model
model_filename = 'stock_prediction_model.pkl'
model = joblib.load(model_filename)


def predict_stock_trade_decision(model, today_features):
    # Predict whether it's a good day to open or close based on today's features
    prediction = model.predict([today_features])

    # Interpret the prediction
    if prediction[0] == 1:
        return "Open"  # Good day to open a position
    else:
        return "Close"  # Good day to close a position


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from the POST request
        data = request.json
        # Assuming the JSON request contains 'features'
        today_features = data['features']

        # Make a prediction using the loaded model
        prediction = predict_stock_trade_decision(model, today_features)

        # Return the prediction as JSON response
        response = {'prediction': prediction}
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
