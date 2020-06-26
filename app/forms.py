from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Gebruikersnaam', validators=[DataRequired()])
    password = PasswordField('Wachtwoord', validators=[DataRequired()])
    remember_me = BooleanField('Hou me ingelogd')
    submit = SubmitField('Log in')


class RegistrationForm(FlaskForm):
    username = StringField('Gebruikersnaam', validators=[DataRequired()])
    password = PasswordField('Wachtwoord', validators=[DataRequired()])
    password2 = PasswordField(
        'Herhaal wachtwoord', validators=[DataRequired(), EqualTo('Wachtwoord')])
    submit = SubmitField('Versturen')

    def validate_username(self, username):
        admin = User.query.filter_by(username=username.data).first()
        if admin is not None:
            raise ValidationError('Kies een andere gebruikersnaam.')
