from flask_user.forms import username_validator, unique_username_validator, password_validator
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, SelectField
from wtforms.validators import DataRequired, EqualTo


alcohol_passed = False


def toggle_alcohol():
    global alcohol_passed
    alcohol_passed = not alcohol_passed


class ResolutionForm(FlaskForm):
    observation = StringField('Observatie', validators=[DataRequired()])
    consideration = StringField('Consideratie', validators=[DataRequired()])
    decision = StringField('Besluit', validators=[DataRequired()])
    before_alcohol = BooleanField('Na alcoholstreep')
    submit = SubmitField('Versturen')

    def __init__(self, *args, **kwargs):
        print(alcohol_passed)
        super(ResolutionForm, self).__init__(*args, **kwargs)
        if alcohol_passed:
            self.before_alcohol.render_kw = {'disabled': ''}
            self.default = True
        else:
            self.default = False


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
