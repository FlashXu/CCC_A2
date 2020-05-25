from flask import Flask, jsonify, abort, request, make_response, redirect, url_for
from flask_cors import CORS
from flasgger import Swagger
from auth import auth
from error_handler import handler as error_handler
from db import bp as db_blueprint
from count import geo_bp, lang_bp, hashtag_bp
from persistance import bp as persistance_blueprint
from utils import template, swagger_config

app = Flask(__name__)

app.register_blueprint(error_handler)
app.register_blueprint(db_blueprint, url_prefix='/db')
app.register_blueprint(geo_bp, url_prefix='/geo')
app.register_blueprint(lang_bp, url_prefix='/lang')
app.register_blueprint(hashtag_bp, url_prefix='/hashtag')
app.register_blueprint(persistance_blueprint, url_prefix='/persist')

CORS(app)
Swagger(app, config=swagger_config, template=template)


@app.route('/shutdown')
def server_shutdown():
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        raise RuntimeError('Not running with the Werkzeug Server')
    shutdown()
    return 'Shutting down...'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
