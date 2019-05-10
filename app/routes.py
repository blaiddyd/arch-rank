from flask import render_template
from app import app, db
from app.forms import Login, SignUp, CitizenReport
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Citizen
from flask import redirect, url_for, flash

def get_links():
    return [
        {
            'text': 'About',
            'path': url_for('about')
        },
        {
            'text': 'Rank',
            'path': url_for('rank')
        },
        {
            'text': 'Login',
            'path': url_for('login')
        }
    ]

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Welcome', links=get_links())

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('feed'))
    form = SignUp()
    if form.validate_on_submit():
        try:
            citizen = Citizen(citizen_id=form.citizen_id.data, name=form.citizen_id.data, score=0)  
            citizen.set_password(form.password.data)
            db.session.add(citizen)
            db.session.commit()
            ('Success in registering user')
            return redirect(url_for('login'))
        except Exception as e:
            print('There was an error creating new user.' + str(e))
    return render_template('signup.html', title='Join Arch', form=form)

@app.route('/feed')
@login_required
def feed():
    return render_template('feed.html', title='Feed', links=get_links())

@app.route('/profile/<citizen_id>')
@login_required
def profile(citizen_id):
    citizen = Citizen.query.filter_by(citizen_id=citizen_id).first_or_404()
    return render_template('profile.html', title='My Profile', links=get_links())

@app.route('/rank')
def rank():
    return render_template('rank.html', title='Ranking', links=get_links())

@app.route('/login',  methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('feed'))
    form = Login()
    if form.validate_on_submit():
        citizen = Citizen.query.filter_by(citizen_id=form.citizen_id.data).first()
        if citizen is None or not citizen.check_password(form.password.data):
            return redirect(url_for('login'))
            flash('Bad login attempt')
        login_user(citizen)
        flash('Good login')
        return redirect(url_for('feed'))
    return render_template('login.html', form=form, links=get_links(), title="Login")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return 'This is about'