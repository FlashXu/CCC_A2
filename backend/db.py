import couchdb
from flask import jsonify, make_response, Blueprint, abort
from auth import auth
from atexit import register
from time import sleep
from threading import Thread
from utils import RedisQueue
import logging
import json
from datetime import datetime


bp = Blueprint('db', __name__)
q = RedisQueue('db', host='redis')


def udb(name='user', url='172.26.131.114:5984', username='admin', password='admin'):
    return couchdb.Server(f'http://{username}:{password}@{url}').__getitem__(name)


def on_startup():
    def acquire_user(threshold=400):
        while True:
            if q.qsize() < threshold:
                rows = db.view('tree/searched', limit=threshold, reduce=False,
                               include_docs=True)[[False]:[False, {}]].rows
                users = []
                for row in rows:
                    user = row.doc
                    user['searched'] = 'queue'
                    users.append(user)

                if not users:   # wait for 5 seconds to next fetch
                    sleep(5)

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
    result = db.update(users)
    logging.warning(
        f'Put back {sum([r[0] for r in result])} users from queue to db.')


# db = udb(url='45.88.195.224:9001')
# db = udb(url='host.docker.internal:5984')
db = udb()
on_startup()


@bp.route('/monitor')
@auth.login_required
def monitor():
    search = []
    for item in db.view('tree/searched', group_level=2):
        search.append({str(item.key): item.value})
    return {'Search': search}


@bp.route('/next_search')
def next_search():
    return q.get()


@bp.route('/queue')
def q_stat():
    return str(q.qsize())


def parse_date(s):
    try:
        return datetime.strptime(s, '%Y-%m-%d') if s else None
    except ValueError:
        abort(400, make_response(
            {'error': f'{s} is not a valid date in format YYYY-MM-DD'}))


@bp.route('/count/<sa>/')
@bp.route('/count/<sa>/<start>/')
@bp.route('/count/<sa>/<start>/<end>/')
def get_count(sa, start='2013-01-01', end=datetime.today().strftime('%Y-%m-%d')):
    cut = [3, 5, 9]
    if len(sa) not in cut:
        abort(400)

    group_level = cut.index(len(sa)) + 1
    start = parse_date(start)
    end = parse_date(end)

    response = db.view('statistic/geo_by_zone',
                       startkey=[sa[:3], sa[3:5], sa[5:],
                                 start.year, start.month, start.day],
                       endkey=[sa[:3], sa[3:5] or {}, sa[5:] or {},
                               end.year or {}, end.month or {}, end.day or {}],
                       group_level=group_level
                       )
    # print(list(response))

    return jsonify(list(response))
