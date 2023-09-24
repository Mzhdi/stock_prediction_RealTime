# Docker Compose Project for Stock Prediction
![Project Architecture](architecture.png)

This project uses Docker Compose to set up a complete environment for Stock Prediction. It includes ZooKeeper, Kafka, producers, consumers, a Flask server, and a PostgreSQL database.

## Prerequisites

Before you begin, make sure you have the following prerequisites installed on your system:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Project Architecture

![Project Architecture](architecture.png)

## Usage

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/your-username/stock-prediction-docker-compose.git
   cd stock-prediction-docker-compose
Create a .env file based on the provided .env.example file. Customize it with your configuration settings.

Build and start the Docker containers:
docker-compose up -d

Access the Flask server at http://localhost:5000 for stock predictions.

Services
ZooKeeper
ZooKeeper is used for distributed coordination and management.

Kafka
Kafka is a distributed streaming platform used for real-time data feeds.

Producer
The producer service sends data to Kafka topics. Customize the producer as needed.

Consumer
The consumer service processes data from Kafka topics. Customize the consumer as needed.

Flask Server
The Flask server provides an API for stock predictions. It depends on Kafka for data.

PostgreSQL
PostgreSQL is used for storing historical stock data. Database configurations are provided in the .env file.

Contributing
Contributions are welcome! If you'd like to contribute to this project, please follow these guidelines:

Fork the repository.
Create a new branch for your feature or bug fix.
Commit your changes and push to your branch.
Create a pull request with a clear description of your changes.
