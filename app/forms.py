from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired

class Login(FlaskForm):
    citizen_id = StringField('Citizen ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    keepsigned = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class SignUp(FlaskForm):
    citizen_id = StringField('Citizen ID', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmPass = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class CitizenReport(FlaskForm):
    reporter = StringField('Your Citizen ID', validators=[DataRequired()])
    traitor = StringField("The Traitor's Citizen ID", validators=[DataRequired()])
    category = SelectField(
        'Type of Treason',
        validators=[DataRequired()],
        choices=[
            ('speaking_ill', 'Speaking Ill of the Supreme Commander'), 
            ('insulting_citizen', 'Insulting a Fellow Citizen'), 
            ('no_celebrating', 'Not Celebrating *Important Holiday*')
        ]
    )
