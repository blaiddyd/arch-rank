from flask import render_template
from app import app
from app.forms import Login, SignUp, CitizenReport

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

@app.route('/login')
def login():
    form = Login()
    return render_template('login.html', title='Login', form=form)
