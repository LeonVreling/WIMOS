import os

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
    USER_ENABLE_EMAIL = False      # Disable email authentication
    USER_ENABLE_USERNAME = True    # Enable username authentication
    USER_REQUIRE_RETYPE_PASSWORD = True    # Simplify register form
    USER_ENABLE_REGISTER = False
    USER_ENABLE_REMEMBER_ME = False
