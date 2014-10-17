import praw 
from flask import Flask, session, request, redirect, url_for, render_template 

r = praw.Reddit(user_agent='karma_farm')
app = Flask(__name__)
app.debug = True 

@app.route('/')
def index():
    return 'Hello world!'

@app.route('/<username>')
def user_info(username):
    user = r.get_redditor(username)
    gen = user.get_comments()
    comments = [] 

    for comment in gen: 
        comments.append(str(comment.author) + '\n' + str(comment.body) + '\n' + str(comment.score) + '\n' + '\n')
    
    return '\n'.join(comments)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)
