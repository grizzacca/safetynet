from flask import Flask

import importlib
import logging
import os


LOGGER = logging.getLogger(__name__)


app = Flask(__name__)


app.config['BACKEND_HOST'] = os.environ['BACKEND_HOST']
app.config['BACKEND_PORT'] = os.environ['BACKEND_PORT']
app.config['API_VERSION'] = os.environ['API_VERSION']

# load dynamically the API version from the environment
api_module = 'api.v' + app.config['API_VERSION'] + '.routes'
loaded_api = importlib.import_module(api_module)

url = "/urlinfo/{0}".format(app.config['API_VERSION'])
app.register_blueprint(loaded_api.api, url_prefix=url)
