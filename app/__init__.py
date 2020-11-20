from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_user import UserManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models

user_manager = UserManager(app, db, models.User, RoleClass=models.Role)

from app import routes

months = ['januari', 'februari', 'maart', 'april', 'mei', 'juni',
          'juli', 'augustus', 'september', 'oktober', 'november', 'december']


# Parse the timestamp to a readable date
def parse_date(date):
    day = str(date.day)
    month = months[date.month - 1]
    year = str(date.year)
    return day + " " + month + " " + year


def today():
    return parse_date(datetime.now())


app.jinja_env.globals.update(parse_date=parse_date)
app.jinja_env.globals.update(today=today)