
import tweepy
import json
from datetime import datetime
from time import sleep
from tweepy.streaming import StreamListener
import utils


api = utils.api()

# CouchDB connection
db = utils.db()
udb = utils.db(name='users')

# Australia bounding box
bounding = [113.338953078, -43.6345972634, 153.569469029, -10.6681857235]


def process(tweet):
    try:
        data = utils.parse_tweet(tweet)
        # save the new tweet
        if data:
            db.save(data)
            print(f'uploading tweets {data["_id"]}')

            user = utils.parse_user(tweet['user'])
            if user:
                udb.save(user)
                print(f'uploading user {user["_id"]}')

    except Exception as e:
        with open('streamlog.txt', 'a') as f:
            msg = f'{data["_id"]}: {repr(e)}\n'
            f.write(msg)



# Create a class inheriting from StreamListener
class TwitterStream(StreamListener):

    def on_data(self, data):
        tweet = json.loads(data, encoding='utf-8')
        # need to filter out the retweets
        if not (tweet['text'].startswith('RT') or tweet['retweeted']):
            process(tweet)
        return True

    def on_error(self, status_code):
        if status_code == 420:
            print('ERROR: Rate limit reached')
        else:
            print(f'ERROR: code {status_code}')

    ''' Rate Limit '''

    def on_timeout(self):
        print('~~~~~~~~Timeout, sleeping for 60 seconds...\n')
        sleep(60)
        return True  # Don't kill the stream


def stream_crawl():
    stream = tweepy.Stream(api.auth, TwitterStream())

    # Starting a Stream
    print("Twitter streaming started... ")
    while True:
        try:
            stream.filter(locations=bounding)
        except KeyboardInterrupt:
            break
        except:
            # sleep 5 seconds and restart
            stream.disconnect()
            sleep(5)


if __name__ == '__main__':
    stream_crawl()
