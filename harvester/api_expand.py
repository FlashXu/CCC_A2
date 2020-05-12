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
            rows = db.view('tree/expanded', limit=worker_size,
                           reduce=False, include_docs=True)[[False, 0]:[False, 0, {}]].rows
            users = []
            for row in rows:
                user = row.doc
                user['expanded'] = 'queue'
                users.append(user)

            if not users:
                time.sleep(5)
                continue

            results = db.update(users)
            for user, (suc, uid, rev) in zip(users, results):
                if suc:
                    user['_rev'] = rev
                    q.put(user)
        else:
            time.sleep(2)


# consumer
def expand(n):
    api = utils.api(n)
    while not stop.isSet():
        try:
            user = q.get_nowait()
        except:
            time.sleep(5)
            continue

        try:
            level = user['level'] + 1
            uid = user["_id"]

            follower_ids = api.followers_ids(user_id=uid, count=5000)
            friend_ids = api.friends_ids(user_id=uid, count=5000)
            ids = list(set(follower_ids) | set(friend_ids))

            for sub_ids in utils.split_every(ids):
                users = api.lookup_users(user_ids=sub_ids)
                parsed_user = utils.bulk_parse_user(
                    [u._json for u in users], level)
                result = db.update(parsed_user)
                success = sum([r[0] for r in result])

                print(
                    f'Key {n:3} {user["_id"]:19} : Raw {len(users):3}  Parse {len(parsed_user):3}  Upload {success}')

            user['expanded'] = True
            db.save(user)

        except Exception as e:
            msg = str(e)
            print(user, msg)
            if any([m in msg for m in ['Max retries exceeded', 'Connection']]):
                user['expanded'] = False
            else:
                user['expanded'] = msg
        finally:
            db.update([user])


def main(worker_size):
    try:
        with ThreadPoolExecutor(max_workers=worker_size + 1) as executor:
            executor.submit(acquire_user)
            for i in range(worker_size):
                executor.submit(expand, i + offset)
    except KeyboardInterrupt:
        print('\nInterupt Detect! Stopping...')
        stop.set()
        users = []
        while not q.empty():
            user = q.get()
            user['expanded'] = False
            users.append(user)
        db.update(users)
        print(f'Put back {len(users)} users from queue to db.')


if __name__ == "__main__":
    worker_size = 60
    offset = 1 * worker_size

    db = utils.db(name='priority_user', url='172.26.133.133:5984')
    # db = utils.db(name='user', url='45.88.195.224:9001')
    # db = utils.db(url='45.88.195.224:9001')
    stop = Event()
    q = Queue(3 * worker_size)
    main(worker_size)
