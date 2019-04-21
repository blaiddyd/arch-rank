from flask import render_template
from app import app

@app.route('/')
@app.route('/index')

def index():
    links = [
        {
            'text': 'Get Started',
            'path': '#'
        },
        {
            'text': 'Log In',
            'path': '#'
        },
        {
            'text': 'How it Works',
            'path': '#'
        },
        {
            'text': 'FAQ',
            'path': '#'
        }
    ]
    return render_template('index.html', title='Welcome', links=links)
