from flask import Flask

app = Flask(__name__, static_folder='../react/build', template_folder='../react/build', static_url_path='')

from app import routes