from flask import render_template
from app import app, db
from app.forms import Login, SignUp, CitizenReport
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Citizen
from flask import redirect, url_for

@app.route('/')
@app.route('/index')

def index():
    links = [
        {
            'text': 'How it Works',
            'path': '#'
        },
        {
            'text': 'FAQ',
            'path': '#'
        },
        {
            'text': 'Citizens of the Month',
            'path': '#'
        },
        {
            'text': 'Login',
            'path': '#'
        }
    ]
    return render_template('index.html', title='Welcome', links=links)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('feed'))
    form = SignUp()
    if form.validate_on_submit():
        citizen = Citizen(citizen_id=form.citizen_id.data)  
        citizen.set_password(form.password.data)
        db.session.add(citizen)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html', title='Join Arch', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('feed'))
    form = Login()
    if form.validate_on_submit():
        citizen = Citizen.query.filter_by(citizen_id=form.citizen_id.data).first()
        if citizen is None or not citizen.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(citizen)
        return redirect(url_for('feed'))
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/feed')
@login_required
def feed():
    return 'You are viewing user feed'

@app.route('/citizen/<citizen_id>')
@login_required
def citizen(citizen_id):
    citizen = Citizen.query.filter_by(citizen_id=citizen_id).first_or_404()
    