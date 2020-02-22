from flask import Blueprint
from flask import request


api = Blueprint('api_v1', __name__)


@api.route('/<path:subpath>')
def test(subpath):
    return "{0}?{1}".format(subpath, request.query_string.decode('utf-8'))
