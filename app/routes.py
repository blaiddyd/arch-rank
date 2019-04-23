from flask import render_template
from app import app

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


