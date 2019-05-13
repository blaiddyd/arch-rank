from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length
from wtforms.fields.html5 import EmailField
from app.models import Citizen

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
    submit = SubmitField('Lodge Your Report')

class CitizenStatus(FlaskForm):
    status = StringField('Write Your Status ')


