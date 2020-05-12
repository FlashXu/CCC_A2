from flask import jsonify, make_response, Blueprint, abort
from datetime import datetime
from bisect import bisect_left
import requests
import utils
import json


bp = Blueprint('language', __name__)
db = utils.db()