import utils
import tweepy
import time
from threading import Event
from concurrent.futures import ThreadPoolExecutor
from traceback import print_exception
from itertools import islice, cycle
from datetime import datetime
import requests
import json


def acquire_user():
    try:
        response = requests.get(f'http://{backend_ip}/db/next_search').content
        return json.loads(response)
    except:
        pass


def user_tweets(api, uid, max_tweet=100000, max_id=None, min_date=datetime(2014, 1, 1)):
    while max_tweet > 0:
        status = api.user_timeline(
            user_id=uid, count=200, max_id=max_id)
        if not status:
            break
        # yield from status[:max_tweet]
        yield from islice(filter(lambda s: not s.created_at < min_date, status), max_tweet)
        max_id = status[-1].id - 1
        if status[-1].created_at < min_date:
            break
        max_tweet -= len(status)


class Counter:
    def __init__(self, threshold=3):
        self.round = 0
        self.geo = 0
        self.total = 0
        self.maximum = 0
        self.threshold = threshold

    def rate(self):
        return 100.0 * self.geo / self.total if self.total else 0.0

    def abort(self):
        return self.round == 4 and self.rate() < 1 or \
            self.round % 10 == 0 and self.rate() < self.threshold

    def update(self, gc, tc):
        self.round += 1
        self.geo += gc
        self.total += tc
        self.maximum = max(self.maximum, self.rate())

    def promote(self, threshold=5):
        return self.geo >= 10 or self.maximum >= threshold or self.rate() >= self.threshold


# consumer
def search():
    token = cycle(range(len(utils.credential)))
    while not stop.isSet():
        user = acquire_user()
        if not user:
            time.sleep(5)
            continue
        try:
            n = next(token)
            api = utils.api(n)
            counter = Counter()
            for statuses in utils.split_every(user_tweets(api, user['_id']), 100):
                parsed_data = utils.bulk_parse_tweet(
                    [s._json for s in statuses])

                if parsed_data:
                    result = db.update(parsed_data)
                    success = sum([r[0] for r in result])
                else:
                    success = 0

                counter.update(len(parsed_data), len(statuses))

                info = f'Key {n:3} {user["_id"]:19} :  Place {len(parsed_data):2}/{len(statuses):3}  Upload {success:2}  Rate {counter.rate():4.1f}%'

                # skip this user if the geo rate is less than threshold
                if counter.abort():
                    print(f'{info}  Abort...')
                    break
                else:
                    print(info)

            # promote the user level for further friends/follower BFS searching
            if counter.promote():
                user['level'] = 0
                print(
                    f'Key {n:3} {user["_id"]:19} :  Maximum {counter.maximum:4.1f}%  Final {counter.rate():4.1f}%  Promote!!!')

            user['searched'] = True
        except Exception as e:
            msg = str(e)
            print(user, msg)
            if any([m in msg for m in ['Max retries exceeded', 'Connection', 'payload']]):
                user['searched'] = False
            else:
                user['searched'] = msg
        finally:
            udb.update([user])


def main(worker_size):
    try:
        with ThreadPoolExecutor(worker_size) as e:
            futures = [e.submit(search) for _ in range(worker_size)]

            def callback(worker):
                e = worker.exception()
                if e:
                    print_exception(type(e), e, e.__traceback__)

            for f in futures:
                f.add_done_callback(callback)

    except KeyboardInterrupt:
        print('\nInterupt Detect! Stopping...')
        stop.set()


if __name__ == "__main__":
    worker_size = 3

    backend_ip = '45.88.195.224:5000'
    db_ip = '45.88.195.224:9001'

    backend_ip = '172.26.132.92:5000'
    db_ip = '172.26.131.114:5984'

    db = utils.db(url=db_ip)
    udb = utils.db(name='users', url=db_ip)

    stop = Event()
    main(worker_size)
