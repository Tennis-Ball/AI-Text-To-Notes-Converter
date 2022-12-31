import config
from flask import Flask


app = Flask(__name__)
app.config.from_object(config.ProdConfig)

from app import routes

