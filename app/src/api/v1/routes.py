from flask import Blueprint
from flask import current_app
from flask import jsonify
from flask import request
from rediscluster import RedisCluster


api = Blueprint('api_v1', __name__)


def get_blacklist_status(original_path):
    startup_nodes = dict()

    startup_nodes['host'] = current_app.config['BACKEND_HOST']
    startup_nodes['port'] = current_app.config['BACKEND_PORT']

    status = None
    try:
        client = RedisCluster(startup_nodes=[startup_nodes])
        status = client.get(original_path)
        if status:
            status = status.decode('utf-8')
        else:
            status = "safe|not listed"
    except Exception:
        return "unverified|internal error"

    return status


@api.route('/<path:subpath>')
def safetycheck(subpath):
    original_path = subpath
    query_string = request.query_string.decode('utf-8')
    if query_string:
        original_path = "{0}?{1}".format(original_path, query_string)
    blacklist_status = get_blacklist_status(original_path)

    return jsonify(url=original_path, status=blacklist_status)
