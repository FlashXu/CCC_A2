from flask import jsonify, make_response, Blueprint, abort, redirect, request
from flasgger import swag_from
import utils


bp = Blueprint('persistance', __name__)

db = utils.db()
udb = utils.db(name='users')


@bp.route('/tweet/', methods=['POST', 'PUT'])
@bp.route('/tweet/<id>', methods=['GET', 'DELETE'])
@swag_from('docs/tweet_get.yml', methods=['GET'])
@swag_from('docs/tweet_post.yml', methods=['POST', 'PUT'])
@swag_from('docs/tweet_delete.yml', methods=['DELETE'])
def tweet(id=None):
    return crud(id, db)


@bp.route('/user/', methods=['POST', 'PUT'])
@bp.route('/user/<id>', methods=['GET', 'DELETE'])
@swag_from('docs/user_get.yml', methods=['GET'])
@swag_from('docs/user_post.yml', methods=['POST', 'PUT'])
@swag_from('docs/user_delete.yml', methods=['DELETE'])
def user(id=None):
    return crud(id, udb)


def crud(id, db):
    if request.method == 'GET':
        try:
            return db[id]
        except:
            abort(404)
    if request.method in ['POST', 'PUT']:
        data = request.get_json()
        try:
            id, rev = db.save(data)
            return {id: rev}
        except Exception as e:
            return make_response(jsonify({'error': 'conflict'}), 400)
    if request.method == 'DELETE':
        try:
            del db[id]
            return make_response(jsonify({id: 'deleted'}), 400)
        except:
            abort(404)
