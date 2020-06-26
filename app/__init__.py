import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_user import UserManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# if not os.path.exists(app.config['UPLOADS']):
#     os.makedirs(app.config['UPLOADS'])

from app import routes, models

user_manager = UserManager(app, db, models.User)
