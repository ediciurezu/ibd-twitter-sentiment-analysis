[23:10] Eduard-Claudiu CIUREZU (101147)
import tweepy
from tweepy.streaming import StreamingClient
from kafka.producer import KafkaProducer

bearer_token = ''
topic_name = 'twitter-streaming-topic'
def send_data():
    print('start sending data from Twitter to socket')
    # start sending data from the Streaming API
    twitter_stream = TweetsListener(bearer_token)
    twitter_stream.add_rules(tweepy.StreamRule('lang:en'))
    twitter_stream.filter()
class TweetsListener(StreamingClient):
    # tweet object listens for the tweets
    def __init__(self, bearer):
        StreamingClient.__init__(self, bearer_token=bearer)
        self.producer = KafkaProducer(bootstrap_servers='localhost:9092')
    def on_tweet(self, tweet):
        try:
            print("new tweet")
            self.producer.send(topic_name, str(tweet).encode('utf-8'))
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
    def on_errors(self, errors):
        print("Received errors: %s" % errors)
        return True
if __name__ == "__main__":
    send_data()

