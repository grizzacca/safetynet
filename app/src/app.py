from flask import Flask
from api.v1.routes import api as api_v1


app = Flask(__name__)


app.register_blueprint(api_v1, url_prefix='/urlinfo/1')
