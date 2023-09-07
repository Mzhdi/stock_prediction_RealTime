from flask import Flask, request, jsonify
import yfinance as yf

app = Flask(__name__)

@app.route('/stock/<symbol>', methods=['GET'])
def get_stock_data(symbol):
    try:
        # Fetch real-time stock data using yfinance
        stock = yf.Ticker(symbol)
        print(stock)
        data = stock.history(period="1d")
        print(data)
        if not data.empty:
            latest_data = data.iloc[-1].to_dict()
            return jsonify(latest_data)
        else:
            return jsonify({'error': 'Unable to fetch data'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

########
