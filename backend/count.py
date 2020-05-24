from flask import jsonify, make_response, Blueprint, abort, request
from datetime import datetime
from bisect import bisect_left
from flasgger import swag_from
from collections import Counter
import requests
import utils
import json


geo_bp = Blueprint('geo', __name__)
lang_bp = Blueprint('language', __name__)
db = utils.db()
sa2 = json.load(open('sa2.json', 'r'))


def parse_date(s):
    try:
        datetime.strptime(s, '%Y-%m-%d')
        return s.split('-')
    except ValueError:
        abort(400, make_response(
            {'error': f'{s} is not a valid date in format YYYY-MM-DD'}))


def build_query(sa2, start, end, **kwargs):
    return {
        'startkey': [*cut(sa2), *start],
        'endkey': [*cut(sa2), *end],
        **kwargs,
    }


def zones_start_with(id):
    id = str(id)
    next_id = str(int(id) + 1)
    return sa2[bisect_left(sa2, id):bisect_left(sa2, next_id)]


def cut(s, cut_point=[3, 5]):
    return [s[i:j] for i, j in zip([None] + cut_point, cut_point + [None])]


def summary(view):
    level = request.args.get('level')
    if not level:
        abort(404)
    if level not in ['1', '2', '3']:
        abort(400)

    count = {}
    for r in db.view(view, group_level=level):
        if r.key:
            key = ''.join(r.key)
            if key != 'und':
                count[key] = r.value
    return count


def summary_with_time(view, sa, start, end, callback):
    if start > end:
        abort(400)

    start = parse_date(start)
    end = parse_date(end)

    detail = request.args.get('detail')
    detail = bool(detail and detail.lower() in ("yes", "true", "t", "1"))
    ddoc, view = view.split('/')
    if len(sa) == 5 and not detail:
        count = {}
        for r in db.view(f'{ddoc}_sa3/{view}', group_level=2, startkey=[*cut(sa, cut_point=[3]), *start], endkey=[*cut(sa, cut_point=[3]), *end]):
            if r.key:
                key = ''.join(r.key)
                if key != 'und':
                    count[key] = r.value
        return count
    else:
        queries = {'queries': [build_query(
            s, start, end, group_level=3) for s in zones_start_with(sa)]}

        url = f'{utils.base()}/tweets/_design/{ddoc}/_view/{view}/queries'
        response = requests.post(url, json=queries).content
        results = json.loads(response)['results']
        rows = [r['rows'][0] for r in results if r['rows']]
        result = {''.join(r['key']): r['value']
                  for r in rows if ''.join(r['key']) != 'und'}
        return result if detail else {sa: callback(result)}


@geo_bp.route('/')
@swag_from('docs/geo_count.yml')
def get_all_count():
    return summary('geo/by_zone')


@geo_bp.route('/<sa>/<start>/<end>/')
@swag_from('docs/geo_time_count.yml')
def get_count(sa, start, end):
    def callback(result):
        return sum([v for v in result.values()])

    return summary_with_time('geo/by_zone', sa, start, end, callback)


@lang_bp.route('/')
@swag_from('docs/lang_count.yml')
def get_all_count():
    return summary('lang/by_zone')


@lang_bp.route('/<sa>/<start>/<end>/')
@swag_from('docs/lang_time_count.yml')
def get_count(sa, start, end):
    def callback(result):
        c = Counter()
        for v in result.values():
            c.update(v)
        del c['und']
        return c

    return summary_with_time('lang/by_zone', sa, start, end, callback)
