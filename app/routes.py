from flask import render_template
from app import app
from app.forms import Login, SignUp, CitizenReport

links = [
        {
            'text': 'Feed',
            'path': '/feed'
        },
        {
            'text': 'Profile',
            'path': '/profile'
        },
        {
            'text': 'Ranking',
            'path': '/rank'
        },
        {
            'text': 'Login',
            'path': '/login'
        }
    ]

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Welcome', links=links)

@app.route('/feed')
def feed():
    return render_template('feed.html', title='Feed', links=links)

@app.route('/profile')
def profile():
    return render_template('profile.html', title='My Profile', links=links)

@app.route('/rank')
def rank():
    return render_template('rank.html', title='Ranking', links=links)

@app.route('/login')
def login():
    form = Login()
    return render_template('login.html', title='Login', form=form)
