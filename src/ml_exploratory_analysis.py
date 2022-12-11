from pyspark.ml import Pipeline
from pyspark.sql import SparkSession
from pyspark.ml.classification import NaiveBayes, LogisticRegression, RandomForestClassifier, DecisionTreeClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import HashingTF, Tokenizer, IDF, StopWordsRemover, CountVectorizer, StringIndexer
from pyspark.sql.functions import *
from pyspark.sql.types import *
from bs4 import BeautifulSoup

spark = SparkSession.builder \
    .appName("ML Analysis") \
    .master("local[*]") \
    .getOrCreate()

schema = StructType([
    StructField("target", IntegerType(), False),
    StructField("ids", LongType(), False),
    StructField("date", StringType(), False),
    StructField("flag", StringType(), False),
    StructField("user", StringType(), False),
    StructField("text", StringType(), False)
])

# Load training data
tweets_csv = spark \
    .read.format("csv") \
    .option("header", "false") \
    .schema(schema) \
    .csv("../data/training.1600000.processed.noemoticon.csv") \
    .select("*") \
    .orderBy(rand()) \
    # .limit(50000)

data = tweets_csv \
    .select("text", col("target").cast("Int").alias("label"))


# Function to clean data
def clean_data(ds: DataFrame) -> DataFrame:
    def html_decoding(text):
        return BeautifulSoup(text, 'html.parser').get_text()

    udf_html_decoding = udf(html_decoding)

    return ds \
        .select(udf_html_decoding(col('text')).alias("text"), "label") \
        .select(regexp_replace(col("text"), "@[A-Za-z0-9_.]+", "").alias("text"), "label") \
        .select(regexp_replace(col("text"), "https?://[A-Za-z0-9./]+", "").alias("text"), "label") \
        .select(regexp_replace(col("text"), "[^a-zA-Z]", " ").alias("text"), "label") \
        .select(trim(col("text")).alias("text"), "label") \
        .select(regexp_replace(col("text"), "\\s\\s+", " ").alias("text"), "label")


# Split data in train and test
splits = data.randomSplit([0.98, 0.02], seed=2000)
train_ds = splits[0]
test_ds = splits[1]

# Clean data
clean_train_ds = clean_data(train_ds)
clean_test_ds = clean_data(test_ds)

# Create pipeline
tokenizer = Tokenizer(inputCol="text", outputCol="words")
stopwords = StopWordsRemover(inputCol="words", outputCol="meaningful_words")
# hashtf = HashingTF(numFeatures=2**16, inputCol="meaningful_words", outputCol='tf')
cv = CountVectorizer(vocabSize=2**16, inputCol="meaningful_words", outputCol='cv')
idf = IDF(inputCol='cv', outputCol="features", minDocFreq=5)
label_stringIdx = StringIndexer(inputCol="label", outputCol="labelIdx")
pipeline = Pipeline(stages=[tokenizer, stopwords, cv, idf, label_stringIdx])

pipelineFit = pipeline.fit(clean_train_ds)
train_df = pipelineFit.transform(clean_train_ds)
test_df = pipelineFit.transform(clean_test_ds)

# LR Model
lr = LogisticRegression(maxIter=100, labelCol="labelIdx")
lrModel = lr.fit(train_df)
predictions = lrModel.transform(test_df)

# # NB Model
# nb = NaiveBayes()
# nbModel = nb.fit(train_df)
# predictions = nbModel.transform(test_df)

# Random Forest Model
# rf = RandomForestClassifier(labelCol="labelIdx")
# rfModel = rf.fit(train_df)
# predictions = rfModel.transform(test_df)

predictions.show(20, False)

accuracy = predictions\
               .filter("labelIdx == prediction")\
               .count() / float(test_df.count())

print(f"Test set accuracy = {accuracy}")

# Accuracy
evaluator = MulticlassClassificationEvaluator(labelCol="labelIdx", predictionCol="prediction", metricName="accuracy")
accuracy = evaluator.evaluate(predictions)
print(f"Test set with evaluator accuracy = {accuracy}")
