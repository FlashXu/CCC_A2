from flask import Flask, jsonify, abort, request, make_response, url_for
from auth import auth
from error_handler import handler as error_handler
from db import bp as db_blueprint

app = Flask(__name__)

app.register_blueprint(error_handler)
app.register_blueprint(db_blueprint, url_prefix='/db')

@app.route('/')
def hello():
    print('hello!!!!')
    return 'hello!'

@app.route('/shutdown')
def server_shutdown():
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        raise RuntimeError('Not running with the Werkzeug Server')
    shutdown()
    return 'Shutting down...'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
