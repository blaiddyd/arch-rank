from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length
from wtforms.fields.html5 import EmailField
from app.models import Citizen

offenses = [('-1000', 'Speaking Ill of the Supreme Commander'), ('-100', 'Insulting a Fellow Citizen'), ('-3000', 'Not Celebrating *Important Holiday*')]
activities = [('2000', 'Graduating from Divine Academy'), ('3000', 'Praising the Supreme Commander'), ('100', 'Contributing to the Community')]

class Login(FlaskForm):
    citizen_id = StringField('Citizen ID', render_kw={"placeholder": "Citizen ID"}, validators=[DataRequired(), Length(min=4, max=8)])
    password = PasswordField('Password', render_kw={"placeholder": "Password"}, validators=[DataRequired()])
    keepsigned = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class SignUp(FlaskForm):
    citizen_id = StringField('Citizen ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmPass = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_id(self, citizen_id):
        citizen = Citizen.query.filter_by(citizen_id=citizen_id.data).first()
        if citizen is not None:
            raise ValidationError('This citizen already exists in Arch')

class CitizenReport(FlaskForm):
    traitor = StringField("The Traitor's Citizen ID", validators=[DataRequired(), Length(min=4, max=8)])
    category = SelectField('Type of Treason', choices=offenses, validators=[DataRequired()])
    body = TextAreaField('More about your report', render_kw={"placeholder": "What do you want to report?"})
    report_submit = SubmitField('Lodge Your Report')

class CitizenStatus(FlaskForm):
    status = TextAreaField("What's on your mind?")
    status_category = SelectField('Type of Activity', choices=activities, validators=[DataRequired()])
    status_submit = SubmitField('Submit Status')


