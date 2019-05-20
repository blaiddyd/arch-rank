from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField  # nopep8
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length
from wtforms.fields.html5 import EmailField
from app.models import Citizen

offenses = [
    ('-3000', 'Speaking Ill of the Supreme Commander'),
    ('-100', 'Insulting a Fellow Citizen'),
    ('-1000', 'Not Celebrating Important Holiday'),
    ('-200', "Insulting the Royal Webmaster's code"),
    ('-2000', 'Conspiring against our Government'),
    ('-500', 'Physical Violence'),
    ('-800', 'Loyalty to Greece'),
    ('-500', 'Defamation'),
    ('-200', 'Being passive-aggressive on Social Media'),
    ('-2000', 'Voting for the oppositon'),
    ('-100', 'Gossiping wrongfully'),
    ('-700', 'Theft'),
    ('-1000', 'Murder'),
    ('500', 'Charity Work'),
    ('1000', 'Praising the Supreme Commander'),
    ('500', 'Working overtime'),
    ('200', 'Contributing to the Community'),
    ('200', "Performing a Citizen's arrest"),
    ('1000', 'Outing a Conspirator')
]
activities = [
    ('5000', 'Graduating from Divine Academy'),
    ('700', 'Praising the Supreme Commander'),
    ('900', 'Contributing to the Community'),
    ('500', 'Charity Work'),
    ('500', 'Working overtime'),
    ('200', 'Contributing to the Community'),
    ('200', "Performing a Citizen's arrest"),
    ('1000', 'Outing a Conspirator')
]


class Login(FlaskForm):
    citizen_id = StringField(
        'Citizen ID',
        render_kw={"placeholder": "Citizen ID"},
        validators=[DataRequired(), Length(min=4, max=8)])
    password = PasswordField(
        'Password',
        render_kw={"placeholder": "Password"},
        validators=[DataRequired()])
    keepsigned = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class SignUp(FlaskForm):
    citizen_id = StringField(
        'Citizen ID',
        render_kw={"placeholder": "Citizen ID"},
        validators=[DataRequired(), Length(min=4, max=8)])
    password = PasswordField(
        'Password',
        render_kw={"placeholder": "Password"},
        validators=[DataRequired()])
    confirmPass = PasswordField(
        'Confirm Password',
        render_kw={"placeholder": "Confirm Password"},
        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_id(self, citizen_id):
        citizen = Citizen.query.filter_by(citizen_id=citizen_id.data).first()
        if citizen is not None:
            raise ValidationError('This citizen already exists in Arch')


class CitizenReport(FlaskForm):
    traitor = StringField(
        "The Traitor's Citizen ID",
        render_kw={"placeholder": "Citizen's ID"},
        validators=[DataRequired(), Length(min=4, max=8)])
    category = SelectField(
        'Type of Treason',
        render_kw={"placeholder": "Select an offense"},
        choices=offenses, validators=[DataRequired()])
    body = TextAreaField(
        'More about your report',
        render_kw={"placeholder": "What would you like to report?"})
    report_submit = SubmitField('Lodge Your Report')


class CitizenStatus(FlaskForm):
    status = TextAreaField(
        "What's on your mind?",
        render_kw={"placeholder": "What are you up to?"})
    status_category = SelectField(
        'Type of Activity',
        choices=activities,
        validators=[DataRequired()])
    status_submit = SubmitField('Submit Status')

class DeleteUser(FlaskForm):
    citizen_id = StringField(
        'Citizen',
        render_kw={"placeholder": "Citizen ID"},
        validators=[DataRequired(), Length(min=4, max=8)])
    delete_submit = SubmitField('Delete Citizen')
