import os
from dotenv import load_dotenv
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('WIMOS_SECRET') or "thisisasecret"

    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}/{}'.format(
        os.environ.get('WIMOS_DB_USERNAME'),
        os.environ.get('WIMOS_DB_PASSWORD'),
        os.environ.get('WIMOS_DB_HOST'),
        os.environ.get('WIMOS_DB_DATABASE'),
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    USER_APP_NAME = "WISO E-moties"      # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = True      # Disable email authentication
    USER_ENABLE_USERNAME = True    # Enable username authentication
    USER_REQUIRE_RETYPE_PASSWORD = True    # Simplify register form
    USER_ENABLE_FORGOT_PASSWORD = True
    USER_ENABLE_REGISTER = False
    USER_ENABLE_REMEMBER_ME = False

    MAIL_SERVER = os.environ.get('WIMOS_MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('WIMOS_MAIL_PORT'))
    MAIL_USE_SSL = os.environ.get('WIMOS_MAIL_USE_SSL') == 'True'
    MAIL_USE_TLS = os.environ.get('WIMOS_MAIL_USE_TLS') == 'True'
    MAIL_USERNAME = os.environ.get('WIMOS_MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('WIMOS_MAIL_PASSWORD')
    USER_EMAIL_SENDER_NAME = os.environ.get('WIMOS_EMAIL_SENDER_NAME')
    USER_EMAIL_SENDER_EMAIL = os.environ.get('WIMOS_EMAIL_SENDER_EMAIL')
