from flask import jsonify, make_response, Blueprint, abort, request
from datetime import datetime
from bisect import bisect_left
from flasgger import swag_from
import requests
import utils
import json


bp = Blueprint('geo', __name__)
db = utils.db()
sa2 = json.load(open('sa2.json', 'r'))


def parse_date(s):
    try:
        datetime.strptime(s, '%Y-%m-%d')
        return s.split('-')
    except ValueError:
        abort(400, make_response(
            {'error': f'{s} is not a valid date in format YYYY-MM-DD'}))


def zones_start_with(id):
    id = str(id)
    next_id = str(int(id) + 1)
    return sa2[bisect_left(sa2, id):bisect_left(sa2, next_id)]


def cut(s, cut_point=[3, 5]):
    return [s[i:j] for i, j in zip([None] + cut_point, cut_point + [None])]


def build_query(sa2, start, end, **kwargs):
    return {
        'startkey': [*cut(sa2), *start],
        'endkey': [*cut(sa2), *end],
        **kwargs,
    }


@bp.route('/')
@swag_from('docs/geo_count.yml')
def get_all_count():
    level = request.args.get('level')
    if not level:
        abort(404)
    if level not in ['1', '2', '3']:
        abort(400)

    count = {}
    for r in db.view('statistic/geo_by_zone', group_level=level):
        if r.key:
            key = ''.join(r.key)
            if key != 'und':
                count[key] = r.value
    return count


@bp.route('/<sa>/<start>/<end>/')
@swag_from('docs/geo_time_count.yml')
def get_count(sa, start, end):
    if start > end:
        abort(400)

    start = parse_date(start)
    end = parse_date(end)

    sa = zones_start_with(sa) if sa else sa2

    queries = {'queries': [build_query(
        s, start, end, group_level=3) for s in sa]}

    url = f'{utils.base()}/tweet/_design/statistic/_view/geo_by_zone/queries'
    response = requests.post(url, json=queries).content
    results = json.loads(response)['results']
    rows = [r['rows'][0] for r in results if r['rows']]
    result = {''.join(r['key']): r['value'] for r in rows}

    return result
