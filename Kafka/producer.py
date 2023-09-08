from kafka import KafkaProducer
import requests
import time


# Define Kafka broker address and topic name
KAFKA_BROKER = 'localhost:9092'
KAFKA_TOPIC = 'stock'
API_KEY = 'RAK70DKX2FXRM7VD'
STOCK_NAME = 'GOOG'
DURATION = '1min'
TIMEOUT = 60000


# Create a KafkaProducer instance
producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER,max_block_ms=TIMEOUT)

# Function to send data to Kafka
def send_data_to_kafka():
    # Convert the string to bytes using UTF-8 encoding
    
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+STOCK_NAME+'&interval='+DURATION+'&apikey='+API_KEY+'&datatype=csv'
    r = requests.get(url)
    if r.status_code == 200:
    # Parse the response content as text and split it into lines
        data = r.text.splitlines()
        producer.send(KAFKA_TOPIC, value=data)
        print("Data sent to Kafka successfully.")
    # producer.flush()

def main():
    try:
        while True:
            send_data_to_kafka()
            time.sleep(70)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        producer.close()

if __name__ == "__main__":
    main()

