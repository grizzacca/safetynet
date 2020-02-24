from flask import Blueprint
from flask import current_app
from flask import jsonify
from flask import request
from rediscluster import RedisCluster
from urllib.parse import urlsplit

import logging


LOGGER = logging.getLogger(__name__)


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
    except Exception as e:
        LOGGER.debug(str(e))

        status = "unverified|internal error"

    return status


@api.route('/<path:subpath>')
def safetycheck(subpath):
    original_path = subpath.rstrip('/')
    url = urlsplit('//' + original_path)

    host = url.hostname

    port = url.port
    if not port:
        return jsonify(url=original_path, status="invalid|port missing")

    LOGGER.info("Looking up host {0} and port {1}".format(host, port))

    query_string = request.query_string.decode('utf-8')
    if query_string:
        original_path = "{0}?{1}".format(original_path, query_string)
    blacklist_status = get_blacklist_status(original_path)

    return jsonify(url=original_path, status=blacklist_status)
