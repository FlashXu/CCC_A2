from flask import jsonify, make_response, Blueprint, abort, redirect, request
from atexit import register
from time import sleep
from threading import Thread
from flasgger import swag_from
import utils
import logging
import json


bp = Blueprint('db', __name__)
search_q = utils.RedisQueue('searched')
expand_q = utils.RedisQueue('expanded')


def on_startup():
    def acquire_user(q, threshold):
        while True:
            try:
                if q.qsize() < threshold:
                    rows = db.view(f'tree/{q.name}', limit=threshold, reduce=False,
                                   include_docs=True)[[False]:[False, {}]].rows
                    users = []
                    for row in rows:
                        user = row.doc
                        user[q.name] = 'queue'
                        users.append(user)

                    if users:   # wait for 5 seconds to next fetch
                        results = db.update(users)
                        logging.warning(
                            f'Put {sum([r[0] for r in results])} into {q.name} queue ...')
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

    Thread(target=acquire_user, daemon=True, args=(search_q, 200,)).start()
    Thread(target=acquire_user, daemon=True, args=(expand_q, 10,)).start()


@register
def on_exit():
    for q in [search_q, expand_q]:
        users = []
        while not q.empty():
            user = json.loads(q.get())
            user['searched'] = False
            users.append(user)
        result = db.update(users)
        logging.warning(
            f'Put back {sum([r[0] for r in result])} users from {q.name} queue to db.')


db = utils.db(name='users')
on_startup()


@bp.route('/monitor/<level>/')
@swag_from('docs/db_monitor.yml')
def monitor(level):
    search = []
    for item in db.view('tree/searched', group_level=level):
        search.append({str(item.key): item.value})
    return {
        '# of Docs': utils.db().info()['doc_count'],
        'Search': search
    }


@bp.route('/next_search')
@swag_from('docs/next_search.yml')
def next_search():
    user = search_q.get_nowait()
    return user if user else {}


@bp.route('/next_expand')
@swag_from('docs/next_expand.yml')
def next_expand():
    user = expand_q.get_nowait()
    return user if user else {}


@bp.route('/queue_stat')
@swag_from('docs/q_stat.yml')
def q_stat():
    return {'search': search_q.qsize(), 'expand': expand_q.qsize()}


@bp.route('/active_tasks')
def active_tasks():
    return redirect(f'{utils.base()}/_active_tasks')

