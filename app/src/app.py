from flask import Flask
# from api.v1.routes import api as api_v1

import importlib
import os


app = Flask(__name__)


app.config['BACKEND_HOST'] = os.environ['BACKEND_HOST']
app.config['BACKEND_PORT'] = os.environ['BACKEND_PORT']
app.config['API_VERSION'] = os.environ['API_VERSION']

api_module = 'api.v' + app.config['API_VERSION'] + '.routes'
loaded_api = importlib.import_module(api_module)

url = "/urlinfo/{0}".format(app.config['API_VERSION'])
app.register_blueprint(loaded_api.api, url_prefix=url)
