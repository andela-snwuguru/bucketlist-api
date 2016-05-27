from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request

app = Flask(__name__)
app.config.from_object('production_config')
db = SQLAlchemy(app)

from app import views