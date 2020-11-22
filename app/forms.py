from flask_user.forms import username_validator, unique_username_validator, password_validator, unique_email_validator
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, SelectField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Email

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
        super(ResolutionForm, self).__init__(*args, **kwargs)
        if alcohol_passed:
            self.before_alcohol.render_kw = {'disabled': ''}
            self.before_alcohol.default = alcohol_passed
            self.before_alcohol.data = alcohol_passed
        else:
            self.before_alcohol.default = alcohol_passed
            self.before_alcohol.data = alcohol_passed


class RegisterBoardMemberForm(FlaskForm):
    """Register new user form."""
    password_validator_added = False

    next = HiddenField()  # for login_or_register.html
    reg_next = HiddenField()  # for register.html

    username = StringField('Gebruikersnaam', validators=[
        DataRequired('Gebruikersnaam is verplicht'),
        username_validator,
        unique_username_validator])
    email = StringField('Email', validators=[
        DataRequired('Email is required'),
        Email('Invalid Email'),
        unique_email_validator])
    password = PasswordField('Wachtwoord', validators=[
        DataRequired('Wachtwoord is verplicht')])
    retype_password = PasswordField('Herhaal wachtwoord', validators=[
        EqualTo('password', message='Wachtwoorden zijn niet hetzelfde')])

    role = SelectField('Rol bij vereniging', choices=[('Bestuurslid', 'Bestuurslid'), ('Kandi', 'Kandi')],
                       validators=[DataRequired('Rol is verplicht')])

    submit = SubmitField('Registreren')

    def validate(self):
        if not super(RegisterBoardMemberForm, self).validate():
            return False
        # All is well
        return True


class RegisterChairmanForm(FlaskForm):
    """Register new user form."""
    password_validator_added = False

    next = HiddenField()  # for login_or_register.html
    reg_next = HiddenField()  # for register.html

    username = StringField('Gebruikersnaam', validators=[
        DataRequired('Gebruikersnaam is verplicht'),
        username_validator,
        unique_username_validator])
    email = StringField('Email', validators=[
        DataRequired('Email is required'),
        Email('Invalid Email'),
        unique_email_validator])
    password = PasswordField('Wachtwoord', validators=[
        DataRequired('Wachtwoord is verplicht')])
    retype_password = PasswordField('Herhaal wachtwoord', validators=[
        EqualTo('password', message='Wachtwoorden zijn niet hetzelfde')])

    association = StringField('Vereniging', validators=[DataRequired('Vereniging is verplicht')])

    submit = SubmitField('Registreren')

    def validate(self):
        if not super(RegisterChairmanForm, self).validate():
            return False
        # All is well
        return True


class LocationAndStartingNumberForm(FlaskForm):
    location = StringField('Locatie', validators=[DataRequired()])
    starting_number = IntegerField('Nummer van eerstvolgende motie', validators=[DataRequired()])
    submit = SubmitField('Opslaan')
