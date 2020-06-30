from flask_user.forms import username_validator, unique_username_validator, password_validator
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, SelectField
from wtforms.validators import DataRequired, EqualTo


class ResolutionForm(FlaskForm):
    observation = StringField('Observatie', validators=[DataRequired()])
    consideration = StringField('Consideratie', validators=[DataRequired()])
    decision = StringField('Besluit', validators=[DataRequired()])
    alcohol = BooleanField('Na alcoholstreep')
    submit = SubmitField('Versturen')


class RegisterForm(FlaskForm):
    """Register new user form."""
    password_validator_added = False

    next = HiddenField()  # for login_or_register.html
    reg_next = HiddenField()  # for register.html

    username = StringField('Gebruikersnaam', validators=[
        DataRequired('Gebruikersnaam is verplicht'),
        username_validator,
        unique_username_validator])
    password = PasswordField('Wachtwoord', validators=[
        DataRequired('Wachtwoord is verplicht'),
        password_validator])
    retype_password = PasswordField('Herhaal wachtwoord', validators=[
        EqualTo('password', message='Wachtwoorden zijn niet hetzelfde')])

    role = SelectField('Rol bij vereniging', choices=[('Bestuurslid', 'Bestuurslid'), ('Kandi', 'Kandi')],
                       validators=[DataRequired('Rol is verplicht')])

    submit = SubmitField('Registreren')

    def validate(self):
        if not super(RegisterForm, self).validate():
            return False
        # All is well
        return True
