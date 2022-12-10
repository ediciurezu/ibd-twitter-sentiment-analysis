from flask import Flask
import boto3
import json
from flask_cors import CORS

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


@app.route('/read/<file>', methods=['GET'])
def read_data(file):
    # Read the data from the S3 bucket
    obj = s3.Object(bucket_name, file)
    body = obj.get()['Body'].read().decode('utf-8')
    return body


if __name__ == '__main__':
    app.run()
