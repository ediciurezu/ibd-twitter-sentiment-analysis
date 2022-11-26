# Project---Introduction-to-Big-Data
 Twitter Sentiment Analysis on Big Data in Spark Framework


## Run zookeeper:
$ bin/zookeeper-server-start.sh config/zookeeper.properties

Another terminal:
$ bin/kafka-server-start.sh config/server.properties

## Create a topic:
$ bin/kafka-topics.sh --create --topic quickstart-events --bootstrap-server localhost:9092
