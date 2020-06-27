from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, EqualTo
from app.models import User


# class LoginForm(FlaskForm):
#     username = StringField('Gebruikersnaam', validators=[DataRequired()])
#     password = PasswordField('Wachtwoord', validators=[DataRequired()])
#     remember_me = BooleanField('Hou me ingelogd')
#     submit = SubmitField('Log in')
#
#
# class RegistrationForm(FlaskForm):
#     username = StringField('Gebruikersnaam', validators=[DataRequired()])
#     password = PasswordField('Wachtwoord', validators=[DataRequired()])
#     password2 = PasswordField(
#         'Herhaal wachtwoord', validators=[DataRequired(), EqualTo('Wachtwoord')])
#     submit = SubmitField('Versturen')
#
#     def validate_username(self, username):
#         admin = User.query.filter_by(username=username.data).first()
#         if admin is not None:
#             raise ValidationError('Kies een andere gebruikersnaam.')

class ResolutionForm(FlaskForm):
    observation = StringField('Observatie', validators=[DataRequired()])
    consideration = StringField('Consideratie', validators=[DataRequired()])
    decision = StringField('Besluit', validators=[DataRequired()])
    alcohol = BooleanField('Na alcoholstreep', validators=[DataRequired()])
    submit = SubmitField('Versturen')