from flask import jsonify, make_response, Blueprint, abort
from datetime import datetime
from bisect import bisect_left
import logging
import utils
import json


bp = Blueprint('zone', __name__)
db = utils.db()
sa2 = json.load(open('sa2.json', 'r'))


def parse_date(s):
    try:
        return datetime.strptime(s, '%Y-%m-%d') if s else None
    except ValueError:
        abort(400, make_response(
            {'error': f'{s} is not a valid date in format YYYY-MM-DD'}))


def zones_start_with(id):
    id = str(id)
    next_id = str(int(id) + 1)
    return sa2[bisect_left(sa2, id):bisect_left(sa2, next_id)]


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
