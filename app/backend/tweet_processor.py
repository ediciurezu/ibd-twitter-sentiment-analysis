import threading
import json

class TwitterFilteringTask(threading.Thread):
    def __init__(self, unprocessed_tweets: list, sentiment: int):
        super(TwitterFilteringTask, self).__init__()
        self.result = None
        self.unprocessed_tweets = unprocessed_tweets
        self.sentiment = sentiment

    def run(self):
        self.result = list(
            map(lambda tweet: tweet['text'],
                filter(lambda tweet: tweet['sentiment'] == self.sentiment, self.unprocessed_tweets)
                )
        )

    def get_data(self):
        return self.result


# Used to process tweet-related information and turn it into statistics
class TweetProcessor:

    @staticmethod
    def process_raw_tweets(data: str) -> str:
        '''
        Turns the raw list of strings into a valid json array of tweets
        '''
        split_data = data.splitlines()
        result = []
        for data in split_data:
            result.append(json.loads(data))
        return result


    @staticmethod
    def get_statistics(unprocessed_tweets: list) -> dict:
        '''
        Creates a json/dict containing statistical data, and two lists containing all positive
            and negative tweets

        Args:
            unprocessed_tweets (list) the list of tweet data

        Returns:
            dict: a JSON containing total tweets, total positive and negative tweets
        '''
        # total_tweets = len(unprocessed_tweets)
        #
        # positive_tweets_filtering_task = TwitterFilteringTask(unprocessed_tweets, 1)
        # negative_tweets_filtering_task = TwitterFilteringTask(unprocessed_tweets, 0)
        #
        # positive_tweets_filtering_task.start()
        # negative_tweets_filtering_task.start()
        #
        # positive_tweets_filtering_task.join()
        # negative_tweets_filtering_task.join()
        #
        # positive_tweets = positive_tweets_filtering_task.get_data()
        # negative_tweets = negative_tweets_filtering_task.get_data()
        #
        # positive_tweets_count = len(positive_tweets)
        # negative_tweets_count = total_tweets - positive_tweets_count

        positive = []
        negative = []
        for data in unprocessed_tweets:
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
            'positive_tweets': positive[-5:],
            'negative_tweets': negative[-5:]
        }
