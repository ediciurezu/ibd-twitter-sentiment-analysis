from pyspark.sql import SparkSession

if __name__ == "__main__":
    packages = [
        'org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1'
    ]
    spark = SparkSession\
        .builder\
        .appName("TwitterSentimentAnalysis") \
        .config("spark.jars.packages", ",".join(packages))\
        .getOrCreate()

    lines = spark.readStream.format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "twitter-streaming-topic") \
        .load()

    df = lines.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

    df.writeStream.queryName("all_tweets") \
        .outputMode("append")\
        .format("console") \
        .option("truncate", False)\
        .start()\
        .awaitTermination()
