import praw 
from flask import Flask, session, request, redirect, url_for, render_template, jsonify 

r = praw.Reddit(user_agent='karma_farm')
app = Flask(__name__)
app.debug = True 
current_api_version = '/api/v0'
@app.route('/')
def index():
    return 'Hello world!'

@app.route(current_api_version + '/<username>', methods=['GET'])
def user_info(username):
    user = r.get_redditor(username)
    gen = user.get_comments()
    comments = [] 

    for comment in gen: 
        comments.append(str(comment.author) + '\n' + str(comment.body) + '\n' + str(comment.score) + '\n' + '\n')
    
    return ''.join(comments)

@app.route(current_api_version + '/user_profile/<username>', methods=['GET'])
def karam_histogram(username):
    user = r.get_redditor(username)
    user_json = {
        '_id' : str(username),
        'comment_karma' : user.comment_karma,
        'link_karma' : user.link_karma
    }    

    return jsonify(user_json)

@app.route('/r/<subreddit>', methods=['GET'])
def first_twentyfive(subreddit):
    submissions = r.get_subreddit(subreddit).get_hot(limit=25)
    result = [str(x) for x in submissions]

    results = ""

    for post in result:
        results += "{}<br/>".format(post)

    return results



        

if __name__ == '__main__':
     app.run('0.0.0.0', port=5000)
