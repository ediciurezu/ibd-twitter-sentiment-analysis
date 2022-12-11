from flask import Flask
import boto3
import json
from flask_cors import CORS

from tweet_processer import TweetProcessor

app = Flask(__name__)
CORS(app)
app.config.from_file("config.json", load=json.load)

# Get config data
config_data = app.config.get("JSON_AS_ASCII")
bucket_name = config_data["bucket_name"]
aws_access_key_id = config_data["aws_access_key_id"]
aws_secret_access_key = config_data["aws_secret_access_key"]

# Connect to the S3 bucket
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)
s3 = session.resource('s3')


# Returns all data from a specific file
@app.route('/read/<file>', methods=['GET'])
def read_data(file):
    # Read the data from the S3 bucket
    obj = s3.Object(bucket_name, file)
    body = obj.get()['Body'].read().decode('utf-8')
    return body


# Returns data from all files
@app.route('/read_all', methods=['GET'])
def read_all_data():
    client = session.client('s3')
    response = client.list_objects_v2(Bucket=bucket_name)

    # Get a list of the objects in the bucket
    objects = response['Contents']

    # Print the names of the objects in the bucket
    result = []
    for obj in objects:
        file_name = obj['Key']
        result += json.loads(read_data(file_name))

    return result


# Returns a dictionary containing total, positive and negative tweets
@app.route('/statistics', methods=['GET'])
def get_statistics():
    unprocessed_tweets = read_all_data()
    return TweetProcessor.get_statistics(unprocessed_tweets)

if __name__ == '__main__':
    app.run()
