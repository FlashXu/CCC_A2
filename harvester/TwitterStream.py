
import tweepy
import json
from datetime import datetime
from time import sleep
from tweepy.streaming import StreamListener
from pprint import pprint
import couchdb

# Variables that contains the user credentials to access Twitter API
consumer_key = 'n5FxlcSsxWpaVrLtdSiHTcWiG'
consumer_secret = 'Tf2Xv6h5Z7bWcTUkhzaxmZfzVF8OeIkzbFi3tjO1wz6KkqRbls'
access_token_key = '1250699207272304640-TAWwK8eToTmHNcAT79RZVIapIFYNla'
access_token_secret = '2PBtpTyUQvr1T3NtgbLHNI6QDdYPloaFvQhP8J49cIkG1'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# CouchDB connection
db = 'tweet-stream'
db_username = 'admin'
db_password = 'admin'
server = couchdb.Server(f'http://{db_username}:{db_password}@localhost:5984')
if db not in server:
    server.create(db)
db = server[db]

# Australia bounding box
bounding = [113.338953078, -43.6345972634, 153.569469029, -10.6681857235]


def process(tweet):
    try:
        # filter all twitter outside Australia
        if not (tweet['place'] and tweet['place']['country_code'] == 'AU'):
            return

        data = {}
        data['_id'] = tweet['id_str']
        data['date'] = datetime.strptime(
            tweet['created_at'], '%a %b %d %H:%M:%S %z %Y').strftime('%Y-%m-%d %H:%M:%S%z')
        data['user'] = tweet['user']['screen_name']
        data['lang'] = tweet['lang']

        def extract_hashtag(entity):
            return [h['text'] for h in entity['hashtags']]

        # extended tweet is un-truncated version of the tweet
        if 'extended_tweet' in tweet:
            ext = tweet['extended_tweet']
            data['text'] = ext['full_text']
            data['hashtags'] = extract_hashtag(ext['entities'])
        else:
            data['text'] = tweet['text']
            data['hashtags'] = extract_hashtag(tweet['entities'])

        # geo-location
        if tweet['coordinates'] and 'coordinates' in tweet['coordinates']:
            data['geo'] = tweet['coordinates']['coordinates']
        elif tweet['geo'] and 'coordinates' in tweet['geo']:
            coordinate = tweet['geo']['coordinates']
            if len(coordinate) == 2:
                data['geo'] = [coordinate[1], coordinate[0]]

        place = tweet['place']
        place_key = ['place_type', 'full_name', 'bounding_box']
        data['place'] = {k: place[k] for k in place if k in place_key}

        print(f'uploading tweets {data["_id"]}')
        db.save(data)

    except Exception as e:
        with open('streamlog.txt', 'a') as f:
            msg = f'{data["_id"]}: {repr(e)}\n'
            print(msg)
            f.write(msg)
            sleep(30)


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
    stream = tweepy.Stream(auth, TwitterStream())

    # Starting a Stream
    print("Twitter streaming started... ")
    # stream.filter(track=list(keyword))
    while True:
        try:
            stream.filter(locations=bounding)
        except:
            # sleep 5 seconds and restart
            stream.disconnect()
            sleep(5)
    


if __name__ == '__main__':
    stream_crawl()
