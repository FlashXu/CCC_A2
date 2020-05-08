import couchdb
from flask import jsonify, make_response, Blueprint, abort
from auth import auth
from atexit import register
from time import sleep
from threading import Thread
from utils import RedisQueue
import logging
import json


bp = Blueprint('db', __name__)
q = RedisQueue('db', host='redis')


def cdb(name='tweet-stream', url='172.26.131.114:5984', username='admin', password='admin'):
    return couchdb.Server(f'http://{username}:{password}@{url}').__getitem__(name)


def on_startup():
    def acquire_user(threshold=800):
        while True:
            if q.qsize() < threshold:
                rows = db.view('user_tree/searched', limit=threshold, reduce=False, sorted=False,
                               startkey=[False], endkey=[False, {}], include_docs=True).rows
                users = []
                for row in rows:
                    user = row.doc
                    user['searched'] = 'queue'
                    users.append(user)
                results = db.update(users)
                logging.warning(
                    f'Put {sum([r[0] for r in results])} into queue ...')
                for user, (suc, uid, rev) in zip(users, results):
                    if suc:
                        user['_rev'] = rev
                        q.put(user)
            else:
                sleep(1)

    Thread(target=acquire_user, daemon=True).start()


@register
def on_exit():
    users = []
    while not q.empty():
        user = json.loads(q.get())
        user['searched'] = False
        users.append(user)
    db.update(users)
    logging.warning(f'Put back {len(users)} users from queue to db.')


# db = cdb(url='45.88.195.224:9001')
# db = cdb(url='127.0.0.1:5984')
db = cdb()
on_startup()


@bp.route('/monitor')
@auth.login_required
def monitor():
    search = []
    for item in db.view('user_tree/searched', group_level=2):
        search.append({str(item.key): item.value})
    return {'Search': search}
    # expand = []
    # for item in db.view('user_tree/expand', group_level=2):
    #     expand.append({str(item.key): item.value})
    # return {'Search': search, 'Expand': expand}


@bp.route('/next_search')
def next_search():
    return q.get()


@bp.route('/queue')
def q_stat():
    return str(q.qsize())