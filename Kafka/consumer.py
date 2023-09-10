from kafka import KafkaConsumer
import psycopg2
import datetime
import DbConnect as db

database = db.DbConnect()

# Define Kafka broker address and topic name
KAFKA_BROKER = 'localhost:9092'
KAFKA_TOPIC = 'stock'

# Define PostgreSQL database connection parameters
db_params = {
    "host": "127.0.0.1",
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
            message_value = message.value[1]
            values = message_value.split(',')
            if len(values) == 6:
                timestamp, open, high, low, close, volume = values

                try:
                    # Define the INSERT statement
                    insert_statement = """
                    INSERT INTO stock (timestamp, open, high, low, close, volume)
                    VALUES (%s, %s, %s, %s, %s, %s);
                    """

                    # Execute the INSERT statement with the message values
                    cursor.execute(insert_statement, (timestamp,
                                   open, high, low, close, volume))
                    conn.commit()

                    print("Inserted a row into the database.")
                except ValueError:
                    print("Error: Invalid data format in the message.")
                    database.insert_one(
                        {'error': 'Invalid data format in the message.'})
            else:
                print("Invalid message format:", message_value)
                database.insert_one({'error': message_value})
        except Exception as e:
            print(f"Error processing message: {str(e)}")
            database.insert_one({'error': str(e)})


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
