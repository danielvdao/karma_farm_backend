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
    
    return ''.join(comments)

@app.route('/karmahist/<username>')
def karam_histogram(username):
    user = r.get_redditor(username)
    gen = user.get_submitted(limit=100)
    karma_by_subreddit = {}
    result = ""

    for thing in gen:
        
        subreddit = thing.subreddit.display_name
        karma_by_subreddit[subreddit] = (karma_by_subreddit.get(subreddit, 0) + thing.score)

    for subreddit, karma in karma_by_subreddit.iteritems():
        result += "{}: {}<br/>".format(subreddit, karma_by_subreddit[subreddit])

    return result


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)
