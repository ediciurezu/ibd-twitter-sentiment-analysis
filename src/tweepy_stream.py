import tweepy


class TweetPrinter(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        print(tweet)


def run_stream(bearer_token):
    printer = TweetPrinter(bearer_token)
    printer.sample()
