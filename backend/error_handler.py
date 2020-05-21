from flask import jsonify, make_response, Blueprint

handler = Blueprint('error_handler', __name__)


@handler.app_errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

@handler.app_errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

