from flask import Blueprint
from flask import jsonify
from flask import request


api = Blueprint('api_v1', __name__)


@api.route('/<path:subpath>')
def test(subpath):
    original_path = subpath
    query_string = request.query_string.decode('utf-8')
    if query_string:
        original_path = "{0}?{1}".format(original_path, query_string)
    return jsonify(url=original_path)
