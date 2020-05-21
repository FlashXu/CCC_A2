from flask_httpauth import HTTPBasicAuth
from flask import jsonify, make_response

auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'COMP90024':
        return 'team22'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog
