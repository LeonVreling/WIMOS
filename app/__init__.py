import os

from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

# if not os.path.exists(app.config['UPLOADS']):
#     os.makedirs(app.config['UPLOADS'])

from app import routes, models
