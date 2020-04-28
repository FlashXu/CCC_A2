import utils
import tweepy
import json
import time
import GetOldTweets3 as got
from concurrent.futures import ThreadPoolExecutor
from threading import Event
from random import random, choice


def upload(results):
    api = choice(utils.credential).api()
    ids = [tweet.id for tweet in results]
    statuses = api.statuses_lookup(ids)
    parsed_data = utils.bulk_parse_tweet(statuses)
    result = db.update(parsed_data)
    success = sum([r[0] for r in result])
    if success:
        print(f'Uploading {success:3} tweets', flush=True)


def buffer(results):
    update_executor.submit(upload, results)


def search(max_tweet=300):
    # get next user to search, the purpose of while loop is handle race condition
    while not stop.isSet():
        while True:
            user = db.view('user_tree/searched', limit=1, reduce=False,
                           startkey=[False], endkey=[False, {}], include_docs=True).rows[0].doc
            try:
                user['searched'] = True
                _, rev = db.save(user)
                break
            except:
                # Race condition... Skip to next available user.
                pass
        try:
            tweetCriteria = got.manager.TweetCriteria().setUsername(
                user['name']).setMaxTweets(max_tweet)
            got.manager.TweetManager.getTweets(tweetCriteria, buffer)
            time.sleep(random() * 5)
        except:
            # HTTP 429 Too many requests, restore the user['searched'] to False
            user['_rev'] = rev
            user['searched'] = False
            db.save(user)
            break


if __name__ == "__main__":
    # db = utils.db()
    db = utils.db(url='115.146.95.16:9001')
    # db = utils.db(url='172.26.131.114:5984')
    worker_size = 5
    stop = Event()
    try:
        with ThreadPoolExecutor(max_workers=worker_size // 2) as update_executor, \
                ThreadPoolExecutor(max_workers=worker_size) as executor:
            for i in range(worker_size):
                executor.submit(search)
                time.sleep(0.2)
    except KeyboardInterrupt:
        print('Interupt Detect! Stopping...')
        stop.set()
