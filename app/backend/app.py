from flask import Flask
import boto3
import json
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from tweet_processor import TweetProcessor
import praw
from langdetect import detect
import pandas as pd
import regex as re
from textblob import TextBlob
import os

# Initialize and configure the Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config.from_file("config.json", load=json.load)
# Initialize the socketio instance
socketio = SocketIO(app, cors_allowed_origins="*", logging=False)

# Get config data
# config_data = app.config.get("JSON_AS_ASCII")
# bucket_name = config_data["bucket_name"]
# aws_access_key_id = config_data["aws_access_key_id"]
# aws_secret_access_key = config_data["aws_secret_access_key"]

# # Connect to the S3 bucket
# session = boto3.Session(
#     aws_access_key_id=aws_access_key_id,
#     aws_secret_access_key=aws_secret_access_key,
# )
# s3 = session.resource('s3')

# Variable which stores the previous data that was sent to the frontend
previousData = {
    'statistics': {
        'total': 0,
        'positive': 0,
        'negative': 0
    },
    'positive_tweets': [],
    'negative_tweets': []
}

# Returns all data from a specific file
# @app.route('/read/<file>', methods=['GET'])
# def read_data(file):
#     # Read the data from the S3 bucket
#     obj = s3.Object(bucket_name, file)
#     body = obj.get()['Body'].read().decode('utf-8')
#     return body

reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    password=os.getenv('REDDIT_PASSWORD'),
    user_agent=os.getenv('REDDIT_USER_AGENT'),
    username=os.getenv('REDDIT_USERNAME'),
)

subreddit = reddit.subreddit("all")


# Returns data from all files
@app.route('/read_all', methods=['GET'])
def read_all_data():
    # client = session.client('s3')
    # response = client.list_objects_v2(Bucket=bucket_name)
    #
    # # Get a list of the objects in the bucket
    # objects = response['Contents']
    # # Keep only .json files from tweets/
    # objects = filter(lambda obj: obj['Key'].startswith('tweets/') \
    #     and obj['Key'].endswith('.json'), objects)

    #

#     result = """{"text":"Who are your current top 11 and post Episode 3 Survey","sentiment":1}
# {"text":"Ripped ear - headgear advice (UK)","sentiment":1}
# {"text":"Turn 12 ticket (1) + downtown bus + great company )","sentiment":1}
# {"text":"Food-policing","sentiment":1}
# {"text":"Have you ever complained?","sentiment":0}
# {"text":"I found theory","sentiment":1}
# {"text":"Some more Batman\u2019s and one more ","sentiment":1}
# {"text":"Rate my swing","sentiment":1}
# {"text":"sometimes its not about the quality... its about the fact that i live in the future and can buy sushi from the grocery store as an american now ","sentiment":1}
# {"text":"Hi, Reddit! It's already autumn in Ukraine, and although the storks have already flown away to warmer climes, but I still want to introduce you one of the symbols of our country. By the way, there are a lot of storks in my neighborhood, which means that good people live here.","sentiment":1}
# {"text":"How to increase watching and subscribers in my YouTube","sentiment":1}
# {"text":"\/r\/TwoXChromosomes \/u\/schparklez i have the thickest leg hair in existence.. should i go for a safety razor or stick with normal plas","sentiment":1}
# {"text":"AC891 FCO to YYZ - Italy Strike","sentiment":1}
# {"text":"Sorority Row 7 (2023) KILL COUNT!","sentiment":1}
# {"text":"George Kao's Take On Email Marketing","sentiment":1}
# {"text":"Insole slipping out of place primus asana","sentiment":0}
# {"text":"Where will Sammy smith end up?","sentiment":1}
# {"text":"I feel so far behind others","sentiment":0}
# {"text":"DCC Dying Earth patron Cazdal","sentiment":1}
# {"text":"Integrating the craft into your life when your life is too busy","sentiment":1}
# {"text":"Lesser known built in Accessibility Features for low vision Windows users!","sentiment":1}
# {"text":"Rockstar Remastering GTA 5 For Xbox And PS5 In Glorious 4K60 With Ray Tracing","sentiment":1}
# {"text":"Constipation and Diarrhoea- had an very unpleasant episode last night","sentiment":0}
# {"text":"Currently in a loop to contact support lol Can anyone help me?","sentiment":1}
# {"text":"34M - How do I clean this up?","sentiment":1}
# {"text":"How long til I get my diamond rewards?","sentiment":0}
# {"text":"Sights and Sounds YouTube Videos","sentiment":1}
# {"text":"1 disoriented rush later","sentiment":1}
# {"text":"\"The Glitch\"","sentiment":1}
# {"text":"23 [M4F] Massachusetts - I\u2019m trying to fuck today (it\u2019s curved)","sentiment":0}
# {"text":"Washer + Dryer Appliances?","sentiment":1}
# {"text":"Why are people comparing Turpentine to No Heart to Speak of?","sentiment":1}
# {"text":"I recommend \u201cEvery Space Marine Legion Explained \u201c","sentiment":1}
# {"text":"Do you guys think that ES6 should bring back some older mechanics from other ES games?","sentiment":1}
# {"text":"so the new ubi blooddragon....","sentiment":1}
# {"text":"bf told his friends one of my secrets","sentiment":1}
# {"text":"Octane for Blender crashes after appending from another file","sentiment":1}
# {"text":"Cinnabon style Cinnamon Roll in NOLA?","sentiment":1}
# {"text":"The Iron Law of Institutions","sentiment":1}
# {"text":"Christmas things in Budapest","sentiment":1}
# {"text":"Eastern Blockage problem.","sentiment":1}
# {"text":"Smallest and highest \u201cconetent conetribution\u201d rewards from avatarbot wins 10k each, in 24 hours.","sentiment":1}
# {"text":"Dell xps 15 9570 in 2023?","sentiment":1}
# {"text":"Have you noticed Purple Pill Debate has become essentially another Blue Pill echo chamber due to the mods abusing their power and banning most of the Red Pillers?","sentiment":1}
# {"text":"Hear me out gang","sentiment":1}
# {"text":"Love this black heels","sentiment":1}
# {"text":"4Chan Leak Allegedly Exposes GTA 6 Lead Characters And Key Map Details","sentiment":0}
# {"text":"How is the situation in Tel Aviv right now?","sentiment":1}
# {"text":" Introducing Versiobit Audit-Proof Versioning for Your Business Documents ","sentiment":1}
# {"text":"Old power supplies","sentiment":1}
# {"text":"Recommend a song about a historical event","sentiment":1}""".split("\n")
#     print(result)
#     return result

    counter = 0
    submission_list = []
    for submission in subreddit.stream.submissions():
        if counter > 10:
            break

        try:
            if is_english(submission.title) and is_english(submission.selftext):
                submission_list = submission_list + [submission.title]
                counter = counter + 1
        except Exception as e:
            print(e)

    submission_df = pd.DataFrame(submission_list)
    submission_df.columns = ['text']
    submission_df['text'] = submission_df['text'].apply(cleanTxt)
    submission_df['text'] = submission_df['text'].apply(remove_emoji)
    submission_df['subjectivity'] = submission_df['text'].apply(get_subjectivity)
    submission_df['polarity'] = submission_df['text'].apply(get_polarity)
    submission_df['sentiment'] = submission_df['polarity'].apply(get_insight)
    submission_df = submission_df[['text', 'sentiment']]
    result = submission_df.to_json(orient='records', lines=True).split('\n')
    return result


    # Print the names of the objects in the bucket
    # result = []
    # for obj in objects:
    #     file_name = obj['Key']
    #     raw_data = read_data(file_name)
    #     data = TweetProcessor.process_raw_tweets(raw_data)
    #     result += data
    # return result


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

    previousData['statistics']['total'] = previousData['statistics']['total'] + currentData['statistics']['total']
    previousData['statistics']['positive'] = previousData['statistics']['positive'] + currentData['statistics']['positive']
    previousData['statistics']['negative'] = previousData['statistics']['negative'] + currentData['statistics']['negative']

    previousData['positive_tweets'] = currentData['positive_tweets']
    previousData['negative_tweets'] = currentData['negative_tweets']

    return previousData


def is_english(text):
    try:
        language = detect(text)
        return language == 'en'
    except:
        # If language detection fails, you can handle it here.
        return False


def get_insight(score):
    if score < 0:
        return '0'
    else:
        return '1'


def get_subjectivity(text):
    return TextBlob(text).sentiment.subjectivity


# Create a function to get Polarity
def get_polarity(text):
    return TextBlob(text).sentiment.polarity


def remove_emoji(string):
    emoji_pattern = re.compile('['
                               u'\U0001F600-\U0001F64F'  # emoticons
                               u'\U0001F300-\U0001F5FF'  # symbols & pictographs
                               u'\U0001F680-\U0001F6FF'  # transport & map symbols
                               u'\U0001F1E0-\U0001F1FF'  # flags (iOS)
                               u'\U00002500-\U00002BEF'  # chinese char
                               u'\U00002702-\U000027B0'
                               u'\U00002702-\U000027B0'
                               u'\U000024C2-\U0001F251'
                               u'\U0001f926-\U0001f937'
                               u'\U00010000-\U0010ffff'
                               u'\u2640-\u2642'
                               u'\u2600-\u2B55'
                               u'\u200d'
                               u'\u23cf'
                               u'\u23e9'
                               u'\u231a'
                               u'\ufe0f'  # dingbats
                               u'\u3030'
                               ']+', flags=re.UNICODE)

    return emoji_pattern.sub(r'', string)


def cleanTxt(text):
    text = re.sub(r'@[A-Za-z0–9]+', '', text)  # Remove @mentions replace with blank
    text = re.sub(r'#', '', text)  # Remove the '#’ symbol, replace with blank
    text = re.sub(r'RT[\s]+', '', text)  # Removing RT, replace with blank
    text = re.sub(r'https?:\/\/\S+', '', text)  # Remove the hyperlinks
    text = re.sub(r':', '', text)  # Remove :
    return text



if __name__ == '__main__':
    socketio.run(app, port=5001)
