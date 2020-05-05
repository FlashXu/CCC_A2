import utils
import tweepy
import time
import sys
from concurrent.futures import ThreadPoolExecutor
from threading import Event
from random import randrange
from queue import Queue


def acquire_user():
    while not stop.isSet():
        if q.qsize() <= worker_size:
            magic_skip = randrange(15 * q.maxsize)
            rows = db.view('user_tree/searched', limit=worker_size, reduce=False, sorted=False,
                           skip=magic_skip, startkey=[False], endkey=[False, {}], include_docs=True).rows
            users = []
            for row in rows:
                user = row.doc
                user['searched'] = 'queue'
                users.append(user)
            results = db.update(users)
            for user, (suc, uid, rev) in zip(users, results):
                if suc:
                    user['_rev'] = rev
                    q.put(user)
        else:
            time.sleep(2)


def user_tweets(api, uid, max_tweet=300, max_id=None):
    while max_tweet > 0:
        status = api.user_timeline(
            user_id=uid[2:], count=200, max_id=max_id)
        if not status:
            break
        yield from status[:max_tweet]
        max_id = status[-1].id - 1
        max_tweet -= len(status)


# consumer
def search(n, max_tweet=300):
    api = utils.api(n)
    while not stop.isSet():
        user = q.get()
        try:
            for statuses in utils.split_every(user_tweets(api, user['_id']), 100):
                parsed_data = utils.bulk_parse_tweet(statuses)
                result = db.update(parsed_data)
                success = sum([r[0] for r in result])
                print(
                    f'Key {n:3} {user["_id"]:21} : Raw {len(statuses):3}  Place {len(parsed_data):2}  Upload {success:2}')
            user['searched'] = True
            db.save(user)
        except Exception as e:
            if 'Not authorized' in str(e):
                user['searched'] = repr(e)
                db.save(user)
            else:
                q.put(user)
            


def main(worker_size):
    try:
        with ThreadPoolExecutor(max_workers=worker_size + 1) as executor:
            executor.submit(acquire_user)
            for i in range(worker_size):
                executor.submit(search, i + offset)
    except KeyboardInterrupt:
        print('\nInterupt Detect! Stopping...')
        stop.set()
        users = []
        while not q.empty():
            user = q.get()
            user['searched'] = False
            users.append(user)
        db.update(users)
        print(f'Put back {len(users)} users from queue to db.')


if __name__ == "__main__":
    worker_size = 18
    offset = int(sys.argv[-1]) * worker_size

    if offset < 0:
        print('Please specify "-e INDEX" before start the container.')
        sys.exit(-1)

    # db = utils.db()
    db = utils.db(url='115.146.95.16:9001')
    # db = utils.db(url='45.88.195.224:9001')
    stop = Event()
    q = Queue(3 * worker_size)
    main(worker_size)
