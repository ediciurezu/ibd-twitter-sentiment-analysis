import pyspark
from utils import *

if __name__ == "__main__":
    packages = [
        'org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1',
        'org.apache.hadoop:hadoop-aws:3.3.1'
    ]
    spark = SparkSession\
        .builder\
        .appName("TwitterSentimentAnalysis") \
        .config("spark.jars.packages", ",".join(packages))\
        .getOrCreate()

    sc = spark.sparkContext
    conf = pyspark.SparkConf().setAll([("spark.hadoop.fs.s3a.access.key", ""),  # secret here
                                       ("spark.hadoop.fs.s3a.secret.key", ""),  # secret here
                                       ("spark.hadoop.fs.s3a.endpoint", "s3.amazonaws.com")])

    sc.stop()

    spark = SparkSession\
        .builder\
        .config(conf=conf)\
        .getOrCreate()

    train_df = read_train_data(spark)
    pipelineModel = fit_pipeline(train_df)

    clean_train_df = pipelineModel.transform(train_df)
    lrModel = fit_lr(clean_train_df)

    print("Training is ready!")

    lines = spark.readStream.format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "twitter-streaming-topic") \
        .load()

    df = lines.select(col("value").cast(StringType()).alias("text"))
    clean_df = clean_data(df)
    prep_df = pipelineModel.transform(clean_df)
    predict_df = lrModel.transform(prep_df)

    predict_df \
        .select("text", col("prediction").cast("Int").alias("sentiment")) \
        .writeStream.queryName("all_tweets") \
        .outputMode("append") \
        .format("json") \
        .option("checkpointLocation", "s3a://test-ibd/checkpoint/") \
        .option("path", "s3a://test-ibd/tweets/") \
        .start() \
        .awaitTermination()
