from flask import Flask
import json
from flask_cors import CORS
from flask_socketio import SocketIO, emit
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

# Variable which stores the previous data that was sent to the frontend
previousData = {
    'statistics': {
        'total': 0,
        'positive': 0,
        'negative': 0
    },
    'positive_posts': [],
    'negative_posts': []
}

reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    password=os.getenv('REDDIT_PASSWORD'),
    user_agent=os.getenv('REDDIT_USER_AGENT'),
    username=os.getenv('REDDIT_USERNAME'),
)

subreddit = reddit.subreddit("all")

# Listen for updates from the React frontend
@socketio.on('GET_UPDATES')
def handle_get_updates():
    # Check for updates to the data in the Amazon S3 bucket
    updates = RedditHandler.checkForUpdates()
    
    if updates:
        # Send the updates to the React frontend
        emit('UPDATE', updates, broadcast=True)


class RedditReader:
    # Returns data from all files
    @staticmethod
    @app.route('/read_all', methods=['GET'])
    def read_all_data():

        counter = 0
        submission_list = []
        for submission in subreddit.stream.submissions():
            if counter > 10:
                break

            try:
                if RedditClassifier.is_english(submission.title) and RedditClassifier.is_english(submission.selftext):
                    submission_list = submission_list + [submission.title]
                    counter = counter + 1
            except Exception as e:
                print(e)

        submission_df = pd.DataFrame(submission_list)
        submission_df.columns = ['text']
        submission_df['text'] = submission_df['text'].apply(RedditClassifier.clean_text)
        submission_df['text'] = submission_df['text'].apply(RedditClassifier.remove_non_text_characters)
        submission_df['subjectivity'] = submission_df['text'].apply(RedditClassifier.get_subjectivity)
        submission_df['polarity'] = submission_df['text'].apply(RedditClassifier.get_polarity)
        submission_df['sentiment'] = submission_df['polarity'].apply(RedditClassifier.get_insight)
        submission_df = submission_df[['text', 'sentiment']]
        result = submission_df.to_json(orient='records', lines=True).split('\n')
        return result
    

class RedditHandler:
    # Returns the most recent statistics
    @staticmethod
    def checkForUpdates():
        global previousData
        # Get the current data from the reddit reader
        currentData = RedditHandler.get_statistics()

        previousData['statistics']['total'] =  currentData['statistics']['total'] + previousData['statistics']['total']
        previousData['statistics']['positive'] = currentData['statistics']['positive'] + previousData['statistics']['positive']
        previousData['statistics']['negative'] = currentData['statistics']['negative'] + previousData['statistics']['negative']

        previousData['positive_posts'] = currentData['positive_posts'] + previousData['positive_posts']
        previousData['negative_posts'] = currentData['negative_posts'] + previousData['negative_posts']

        return previousData
    
    # Returns a dictionary containing total, positive and negative reddit posts
    @staticmethod
    @app.route('/statistics', methods=['GET'])
    def get_statistics():
        unprocessed_posts = RedditReader.read_all_data()
        return RedditProcessor.process_statistics(unprocessed_posts)

class RedditClassifier:

    @staticmethod
    def is_english(text):
        try:
            language = detect(text)
            return language == 'en'
        except:
            # If language detection fails, you can handle it here.
            return False

    @staticmethod
    def get_insight(score):
        if score < 0:
            return '0'
        else:
            return '1'

    @staticmethod
    def get_subjectivity(text):
        return TextBlob(text).sentiment.subjectivity

    @staticmethod
    # Create a function to get Polarity
    def get_polarity(text):
        return TextBlob(text).sentiment.polarity

    @staticmethod
    def remove_non_text_characters(text):
        text_pattern = re.compile('['
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

        return text_pattern.sub(r'', text)

    @staticmethod
    def clean_text(text):
        text = re.sub(r'@[A-Za-z0–9]+', '', text)  # Remove @mentions replace with blank
        text = re.sub(r'#', '', text)  # Remove the '#’ symbol, replace with blank
        text = re.sub(r'RT[\s]+', '', text)  # Removing RT, replace with blank
        text = re.sub(r'https?:\/\/\S+', '', text)  # Remove the hyperlinks
        text = re.sub(r':', '', text)  # Remove :
        return text

# Used to process reddit-related information and turn it into statistics
class RedditProcessor:

    @staticmethod
    def process_raw_reddit_posts(data: str) -> str:
        '''
        Turns the raw list of strings into a valid json array of reddit posts
        '''
        split_data = data.splitlines()
        result = []
        for data in split_data:
            result.append(json.loads(data))
        return result


    @staticmethod
    def process_statistics(unprocessed_posts: list) -> dict:
        '''
        Creates a json/dict containing statistical data and two lists containing all positive
            and negative reddit posts

        Args:
            unprocessed_posts (list) the list of reddit data

        Returns:
            dict: a JSON containing total reddit posts, total positive and negative reddit posts
        '''

        positive = []
        negative = []
        for data in unprocessed_posts:
            try:
                json_data = json.loads(data)
                print(f'decoding: {json_data}')
                if json_data['sentiment'] == '1':
                    positive.append(json_data['text'])
                else:
                    negative.append(json_data['text'])
            except:
                print(f'Error decoding: {data}')

        return {
            'statistics': {
                'total': len(positive) + len(negative),
                'positive': len(positive),
                'negative': len(negative)
            },
            'positive_posts': positive[-5:],
            'negative_posts': negative[-5:]
        }



if __name__ == '__main__':
    socketio.run(app, port=5001)
