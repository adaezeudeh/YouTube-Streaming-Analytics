# YouTube-Streaming-Analytics
Contains a data streaming application that uses Kafka to simulate sequential records from the Trending YouTube Video dataset. The data is stored in PostgreSQL, and aggregate statistics are generated in real-time. The app is containerized using Docker Compose, and includes API endpoints for querying individual records and aggregate statistics

# YouTube Trending Data API
This is a Flask-based API that allows you to stream and query YouTube trending video data. The data is sourced from the Trending YouTube Video Statistics dataset on Kaggle.

# Features
Stream YouTube trending data sequentially with a user-configurable time delay
Store data to a PostgreSQL database
Aggregate statistics in real-time by channel_title attribute
Query individual records by one or more attributes
Query aggregate statistics by channel
Containerized with Docker

# Technology Stack
Python 3.8
Flask
PostgreSQL
Kafka
Docker

# Streaming Process
This API uses Kafka to simulate a streaming process that sequentially sends data from the YouTube Trending dataset to a PostgreSQL database. The producer.py script reads the data from the files,merges them and sends it to the youtube Kafka topic. The consumer.py script reads the data from the youtube topic, adds a user-configurable delay (default 10 seconds), and writes the data to a PostgreSQL database.

# Endpoints
/views?channel=<channel-name>: returns aggregated views data by channel. If no channel is specified, returns data for all channels.
/likes?channel=<channel-name>: returns aggregated likes data by channel. If no channel is specified, returns data for all channels.
/record?title=<video-title>: returns individual records by video title. Searches the title column using a case-insensitive LIKE operator with wildcard matching.
