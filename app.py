
from flask import Flask, session, request, redirect, url_for, render_template 

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello world!'

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)
