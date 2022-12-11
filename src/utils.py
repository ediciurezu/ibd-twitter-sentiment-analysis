from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.classification import LogisticRegression, LogisticRegressionModel
from pyspark.ml.feature import Tokenizer, StopWordsRemover, CountVectorizer, IDF, StringIndexer
from pyspark.sql import SparkSession

from pyspark.sql.functions import *
from bs4 import BeautifulSoup
from pyspark.sql.types import *


def clean_data(ds: DataFrame) -> DataFrame:
    def html_decoding(text):
        return BeautifulSoup(text, 'html.parser').get_text()

    udf_html_decoding = udf(html_decoding)

    return ds \
        .select(udf_html_decoding(col('text')).alias("text")) \
        .select(regexp_replace(col("text"), "@[A-Za-z0-9_.]+", "").alias("text")) \
        .select(regexp_replace(col("text"), "https?://[A-Za-z0-9./]+", "").alias("text")) \
        .select(regexp_replace(col("text"), "[^a-zA-Z]", " ").alias("text")) \
        .select(trim(col("text")).alias("text")) \
        .select(regexp_replace(col("text"), "\\s\\s+", " ").alias("text")) \
        .select(regexp_replace(col("text"), "^RT ", "").alias("text"))


def clean_train_data(df: DataFrame) -> DataFrame:
    def html_decoding(text):
        return BeautifulSoup(text, 'html.parser').get_text()

    udf_html_decoding = udf(html_decoding)

    return df \
        .select(udf_html_decoding(col('text')).alias("text"), "label") \
        .select(regexp_replace(col("text"), "@[A-Za-z0-9_.]+", "").alias("text"), "label") \
        .select(regexp_replace(col("text"), "https?://[A-Za-z0-9./]+", "").alias("text"), "label") \
        .select(regexp_replace(col("text"), "[^a-zA-Z]", " ").alias("text"), "label") \
        .select(trim(col("text")).alias("text"), "label") \
        .select(regexp_replace(col("text"), "\\s\\s+", " ").alias("text"), "label")


def fit_pipeline(train_df: DataFrame) -> PipelineModel:
    tokenizer = Tokenizer(inputCol="text", outputCol="words")
    stopwords = StopWordsRemover(inputCol="words", outputCol="meaningful_words")
    cv = CountVectorizer(vocabSize=2**16, inputCol="meaningful_words", outputCol='cv')
    idf = IDF(inputCol='cv', outputCol="features", minDocFreq=5)
    label_string_idx = StringIndexer(inputCol="label", outputCol="labelIdx")
    pipeline = Pipeline(stages=[tokenizer, stopwords, cv, idf, label_string_idx])

    return pipeline.fit(train_df)


def read_train_data(spark: SparkSession) -> DataFrame:
    schema = StructType([
        StructField("target", IntegerType(), False),
        StructField("ids", LongType(), False),
        StructField("date", StringType(), False),
        StructField("flag", StringType(), False),
        StructField("user", StringType(), False),
        StructField("text", StringType(), False)
    ])

    # Load training data
    df = spark \
        .read.format("csv") \
        .option("header", "false") \
        .schema(schema) \
        .csv("../data/training.1600000.processed.noemoticon.csv") \
        .select("*") \
        .orderBy(rand()) \
        .select("text", col("target").cast("Int").alias("label"))

    return clean_train_data(df)


def fit_lr(train_df: DataFrame) -> LogisticRegressionModel:
    return LogisticRegression(maxIter=100, labelCol="labelIdx").fit(train_df)
