from flask import Flask
import boto3
import json
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from tweet_processer import TweetProcessor

# Initialize and configure the Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config.from_file("config.json", load=json.load)
# Initialize the socketio instance
socketio = SocketIO(app, cors_allowed_origins="*", logging=False)

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

# Variable which stores the previous data that was sent to the frontend
previousData = None

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


# Listen for updates from the React frontend
@socketio.on('GET_UPDATES')
def handle_get_updates():
    # Check for updates to the data in the Amazon S3 bucket
    updates = checkForUpdates()
    if updates:
        # Send the updates to the React frontend
        emit('UPDATE', updates, broadcast=True)


# Check for updates to the data in the Amazon S3 bucket
def checkForUpdates():
    global previousData
    # Get the current data from the Amazon S3 bucket
    currentData = get_statistics()

    # Compare the current data with the previously stored data
    if currentData == previousData:
        # If there are no updates, return an empty dict
        return {}
    else:
        # If there are updates, store the current data and return the updates
        previousData = currentData
        return currentData
  


if __name__ == '__main__':
    socketio.run(app, port=5001)
