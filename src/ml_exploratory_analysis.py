from pyspark.sql import SparkSession
from pyspark.ml.classification import NaiveBayes
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import HashingTF, Tokenizer, StopWordsRemover
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
    .csv("../data/training.1600000.processed.noemoticon.csv")

# Trim and clean data of spaces
reg_exp = "\\s\\s+"
data = tweets_csv \
    .select("text", col("target").cast("Int").alias("label"))

# Split the data into train and test
splits = data.randomSplit([0.6, 0.4], 1234)
train = splits[0]
test = splits[1]
train_rows = train.count()
test_rows = test.count()

print(f"Training data rows: {train_rows}")
print(f"Testing data rows: {test_rows}")

train.show(10, False)


# HTML decoding
def html_decoding(text):
    return BeautifulSoup(text, 'html.parser').get_text()


udf_html_decoding = udf(html_decoding)

htmlDecodedTrain = train.select(udf_html_decoding(col('text')).alias("text"), "label")

# Remove mentions
removeMentionsTrain = htmlDecodedTrain.select(regexp_replace(col("text"), "@[A-Za-z0-9_.]+", "").alias("text"), "label")

# Remove URLs
removeURLTrain = removeMentionsTrain.select(regexp_replace(col("text"), "https?://[A-Za-z0-9./]+", "").alias("text"), "label")

# Remove hashtags, numbers, punctuation
onlyLettersTrain = removeURLTrain.select(regexp_replace(col("text"), "[^a-zA-Z]", " ").alias("text"), "label")


# Trim and clean data of spaces
cleanTrain = onlyLettersTrain \
    .select(trim(col("text")).alias("text"), "label") \
    .select(regexp_replace(col("text"), reg_exp, " ").alias("text"), "label")
cleanTrain.show(10, False)

# Tokenize data
tokenizer = Tokenizer(inputCol="text", outputCol="words")
tokenizedTrain = tokenizer.transform(cleanTrain)
tokenizedTrain.show(10, False)

# Removing stop words
swr = StopWordsRemover(inputCol=tokenizer.getOutputCol(), outputCol="meaningful_words")
swrTrain = swr.transform(tokenizedTrain)

# Hashing feature
hashTf = HashingTF(inputCol=swr.getOutputCol(), outputCol="features")
numericTrain = hashTf.transform(swrTrain).select(
    'label', 'meaningful_words', 'features'
)

# Train model
nb = NaiveBayes(featuresCol="features", labelCol="label", smoothing=1.0, modelType="multinomial")
model = nb.fit(numericTrain)
print("Training is done!")

# Prepare testing data
cleanTest = test\
    .select(udf_html_decoding(col('text')).alias("text"), "label") \
    .select(regexp_replace(col("text"), "@[A-Za-z0-9_.]+", "").alias("text"), "label") \
    .select(regexp_replace(col("text"), "https?://[A-Za-z0-9./]+", "").alias("text"), "label") \
    .select(regexp_replace(col("text"), "[^a-zA-Z]", " ").alias("text"), "label") \
    .select(trim(col("text")).alias("text"), "label") \
    .select(regexp_replace(col("text"), reg_exp, " ").alias("text"), "label")

cleanTest.show(10, False)

tokenizedTest = tokenizer.transform(cleanTest)
swrTest = swr.transform(tokenizedTest)
numericTest = hashTf.transform(swrTest).select(
    'label', 'meaningful_words', 'features'
)

# Predict
predictions = model.transform(numericTest)
predictions.show(5, False)

# Accuracy
evaluator = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="accuracy")
accuracy = evaluator.evaluate(predictions)
print(f"Test set accuracy = {accuracy}")
