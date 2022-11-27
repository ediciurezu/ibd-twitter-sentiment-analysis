from pyspark.sql import SparkSession
from pyspark.ml.classification import NaiveBayes
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import HashingTF, Tokenizer, StopWordsRemover
from pyspark.sql.functions import *
from pyspark.sql.types import *

spark = SparkSession.builder\
    .appName("ML Analysis")\
    .master("local[*]")\
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
    .read.format("csv")\
    .option("header", "false")\
    .schema(schema)\
    .csv("../data/training.1600000.processed.noemoticon.csv") #Sentiment140 dataset

# Trim and clean data of spaces
reg_exp = "\\s\\s+"
data = tweets_csv\
    .select("text", col("target").cast("Int").alias("label"))\
    .select(trim(col("text")).alias("text"), "label")\
    .select(regexp_replace(col("text"), reg_exp, " ").alias("text"), "label")

# Split the data into train and test
splits = data.randomSplit([0.6, 0.4], 1234)
train = splits[0]
test = splits[1]
train_rows = train.count()
test_rows = test.count()

print(f"Training data rows: {train_rows}")
print(f"Testing data rows: {test_rows}")

# Tokenize data
tokenizer = Tokenizer(inputCol="text", outputCol="words")
tokenizedTrain = tokenizer.transform(train)
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
tokenizedTest = tokenizer.transform(test)
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
