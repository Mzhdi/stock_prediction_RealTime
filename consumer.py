from kafka import KafkaConsumer
import psycopg2
import datetime
import DbConnect as db
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

database = db.DbConnect()

# Define Kafka broker address and topic name
load_dotenv()

KAFKA_BROKER = os.getenv("KAFKA_HOST") + ':' + '9092'
KAFKA_TOPIC = 'stock'
FLASK_HOST = os.getenv("FLASK_SERVER_HOST")

# Define PostgreSQL database connection parameters
db_params = {
    "host": "postgres",
    "database": "Stock_hist",
    "user": "postgres",
    "password": "zerouk1234"
}

# Create a KafkaConsumer instance
consumer = KafkaConsumer(
    KAFKA_TOPIC, bootstrap_servers=KAFKA_BROKER, group_id='my-group')

# Establish a database connection
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# Function to consume and process messages from Kafka and insert into PostgreSQL


def consume_messages_from_kafka_and_insert():
    for message in consumer:
        try:
            # Process the message value (assuming it's in the format 'timestamp,open,high,low,close,volume')
            message_value = message.value.decode('utf-8')
            values = message_value.split(',')
            if len(values) == 6:
                timestamp, open, high, low, close, volume = values
                data = {'features': [float(open), float(
                    high), float(low), float(close), float(volume)]}
                dataTrain = {'stock_symbol': 'GOOG',
                             'start_date': '2022-01-01', 'end_date': '2022-12-31'}

                try:
                    train = requests.post(
                        url='http://' + FLASK_HOST + ':5000/train',
                        json=dataTrain
                    )
                    print(train.text)

                    response = requests.post(
                        url='http://' + FLASK_HOST + ':5000/predict', json=data)
                    print(response.text)
                    prediction = response.json()['prediction']
                    print(prediction)

                    # Define the INSERT statement
                    insert_statement = """
                    INSERT INTO stock (timestamp, open, high, low, close, volume,prediction)
                    VALUES (%s, %s, %s, %s, %s, %s,%s)
                    """

                    # Execute the INSERT statement with the message values
                    cursor.execute(insert_statement, datetime.strptime((timestamp, "%Y-%m-%d "),
                                   float(open), float(high), float(low), float(close), float(volume), prediction))
                    conn.commit()

                    print("Inserted a row into the database.")
                except ValueError:
                    print("Error: Invalid data format in the message.")
                    database.insert_one(
                        {'error': 'Invalid data format in the message.''http://' + FLASK_HOST + ':5000/predict'})
            else:
                print("Invalid message format:", message_value)
                database.insert_one(
                    {'error': message_value + 'http://' + FLASK_HOST + ':5000/predict'})
        except Exception as e:
            print(f"Error processing message: {str(e)}")
            database.insert_one(
                {'error': str(e)+'http://' + FLASK_HOST + ':5000/predict'})


def main():
    try:
        consume_messages_from_kafka_and_insert()
        print("CSV data saved.")
    except KeyboardInterrupt:
        print("Consumer interrupted.")
        database.insert_one({'error': 'Consumer interrupted.'})
    finally:
        consumer.close()
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()
