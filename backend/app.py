from flask import Flask, jsonify, abort, request, make_response, redirect, url_for
from flasgger import Swagger
from auth import auth
from error_handler import handler as error_handler
from db import bp as db_blueprint
from count import geo_bp as geo_blueprint, lang_bp as lang_blueprint
from utils import template, swagger_config

app = Flask(__name__)

app.register_blueprint(error_handler)
app.register_blueprint(db_blueprint, url_prefix='/db')
app.register_blueprint(geo_blueprint, url_prefix='/geo')
app.register_blueprint(lang_blueprint, url_prefix='/lang')


Swagger(app, config=swagger_config, template=template)


@app.route('/shutdown')
def server_shutdown():
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        raise RuntimeError('Not running with the Werkzeug Server')
    shutdown()
    return 'Shutting down...'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
