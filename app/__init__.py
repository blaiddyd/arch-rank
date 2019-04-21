import os

from flask import Flask

app = Flask(__name__)

@app.route('/')
def test():
    return 'Pls work'

if __name__ == '__main__':
    app.run()