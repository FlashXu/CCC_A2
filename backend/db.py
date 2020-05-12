import couchdb
from flask import jsonify, make_response, Blueprint, abort
from auth import auth
from atexit import register
from time import sleep
from threading import Thread
import utils
import logging
import json


bp = Blueprint('db', __name__)
q = utils.RedisQueue('db', host='redis')


def on_startup():
    def acquire_user(threshold=400):
        while True:
            try:
                if q.qsize() < threshold:
                    rows = db.view('tree/searched', limit=threshold, reduce=False,
                                   include_docs=True)[[False]:[False, {}]].rows
                    users = []
                    for row in rows:
                        user = row.doc
                        user['searched'] = 'queue'
                        users.append(user)

                    if users:   # wait for 5 seconds to next fetch
                        results = db.update(users)
                        logging.warning(
                            f'Put {sum([r[0] for r in results])} into queue ...')
                        for user, (suc, uid, rev) in zip(users, results):
                            if suc:
                                user['_rev'] = rev
                                q.put(user)
                    else:
                        sleep(5)
                else:
                    sleep(1)
            except Exception as e:
                logging.error(repr(e))
                sleep(1)

    Thread(target=acquire_user, daemon=True).start()


@register
def on_exit():
    users = []
    while not q.empty():
        user = json.loads(q.get())
        user['searched'] = False
        users.append(user)
    result = db.update(users)
    logging.warning(
        f'Put back {sum([r[0] for r in result])} users from queue to db.')


db = utils.db(name='priority_user')
# on_startup()


@bp.route('/monitor/<level>/')
def monitor(level):
    """
    This is the monitor of the database.
    ---
    tags:
      - db
    parameters:
      - in: path
        name: level
        description: Aggregate level of user tree
        enum: [1, 2]
        default: 1
        required: true
    responses:
      200:
        description: Number of documents in the database,
         and the worker status of timeline miner.
        
    """
    search = []
    for item in db.view('tree/searched', group_level=level):
        search.append({str(item.key): item.value})
    return {
        '# of Docs': utils.db().info()['doc_count'],
        'Search': search
    }


@bp.route('/next_search')
def next_search():
    user = q.get_nowait()
    return user if user else {}


@bp.route('/queue')
def q_stat():
    return str(q.qsize())
