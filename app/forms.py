from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, DateField, IntegerField  # nopep8
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length
from wtforms.fields.html5 import EmailField
from app.models import Citizen

offenses = [
    ('-1000', 'Speaking Ill of the Supreme Commander'),
    ('-2000', 'Being such a bad citizen that the world hates you also you were adopted'),  # nopep8
    ('-100', 'Insulting a Fellow Citizen'),
    ('-3000', 'Not Celebrating *Important Holiday*')
]
activities = [
    ('5000', 'Graduating from Divine Academy'),
    ('700', 'Praising the Supreme Commander'),
    ('900', 'Contributing to the Community')
]
professions = [
    ('', 'Select your profession'),
    (1, 'High Priest'),
    (1, 'Royal Accountant'),
    (1, 'Industrial Overseer'),
    (1, 'High Court Scientist'),
    (1, 'Counsel Advisor'),
    (1, 'Traitor Hunter'),
    (1, 'Mind Seer'),
    (1, 'Royal Webmaster'),
    (2, 'Personel Manager'),
    (2, 'Comissioned Artist'),
    (2, 'Ferryman'),
    (2, 'Archival Custodian'),
    (2, 'Public Lawyer')
]
islands = [
    ('', 'Select your island'),
    (1, 'Santorini'),
    (1, 'Samos'),
    (1, 'Mykonos'),
    (1, 'Delos'),
    (1, 'Nisyros'),
    (1, 'Izmir'),
    (1, 'Symi'),
    (2, 'Chios'),
    (2, 'Rhodes'),
    (2, 'Kos'),
    (2, 'Samothrace'),
    (2, 'Leros'),
    (2, 'Thasos'),
    (3, 'Lemnos'),
    (3, 'Icaria'),
    (3, 'Naxos'),
    (3, 'Andros'),
    (3, 'Euboea'),
    (3, 'Amorgos'),
    (4, 'Patmos'),
    (4, 'Milos'),
    (4, 'Karpathos'),
    (4, 'Skyros'),
    (4, 'Skiathos'),
    (4, 'Kalymnos'),
    (5, 'Hydra'),
    (6, 'Syros')
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
        validators=[DataRequired()])
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
            raise ValidationError('This citizen is already registered')


class CitizenReport(FlaskForm):
    traitor = StringField(
        "The Traitor's Citizen ID",
        render_kw={"placeholder": "Traitor ID"},
        validators=[DataRequired(), Length(min=4, max=8)])
    category = SelectField(
        'Type of Treason',
        render_kw={"placeholder": "Select an offense"},
        choices=offenses,
        validators=[DataRequired()])
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


class Eval(FlaskForm):
    full_name = StringField(
        "Full Name",
        render_kw={
            "placeholder": "Full Name",
            "data-validation": "custom",
            "data-validation-regexp": "^([a-zA-Z]+)( ([a-zA-Z]+))+$",
            "data-validation-error-msg": " "},
        validators=[DataRequired()])
    birth_date = DateField(
        'DOB',
        format='%d-%m-%Y',
        render_kw={
            "type": "date",
            "data-validation": "date",
            "data-validation-error-msg": " "},
        validators=[DataRequired()])
    home_address = StringField(
        'Home Address',
        render_kw={
            "placeholder": "45 Highcourt Pl",
            "data-validation": "custom",
            "data-validation-regexp": "^([a-zA-Z0-9]+)( ([a-zA-Z]+))+$",  # nopep8
            "data-validation-error-msg": " "},
        validators=[DataRequired()])
    island = SelectField(
        'Island',
        render_kw={
            "data-validation": "required",
            "data-validation-error-msg": " "},
        choices=islands,
        validators=[DataRequired()])
    profession = SelectField(
        'Profession',
        render_kw={
            "data-validation": "required",
            "data-validation-error-msg": " "},
        choices=professions,
        validators=[DataRequired()])
    income = IntegerField(
        'Income',
        render_kw={
            "type": "number",
            "data-validation": "custom",
            "data-validation-regexp": "^([0-9]+)$",
            "step": "1000",
            "data-validation-error-msg": " "},
        validators=[DataRequired()])
    married = BooleanField('Are you married?')
    kids = SelectField(
        'How many kids do you have?',
        choices=[
            (0, 'I have no children'),
            (1, 'I have but one child'),
            (2, 'I have two lovely children'),
            (3, 'There are three children in my household'),
            (4, 'Four children have graced my life with their smiles'),
            (5, 'Not four but five! Five children are there to greet me when I wake'),  # nopep8
            (6, 'The number of children I have is more than five but less than seven alas'),  # nopep8
            (7, 'I have one child for each day of the beautiful week and I have named them accordingly'),  # nopep8
            (8, 'My children are bountiful as the apples on the trees, as the islands of Agea, as the eight wise elders'),  # nopep8
            (9, 'I have nine children')],
        render_kw={
            "data-validation": "required",
            "data-validation-error-msg": " "},
        validators=[DataRequired()])
    lonely = BooleanField(
        'Are you lonely?',
        default=True)
    eval_submit = SubmitField('Submit for evaluation')
