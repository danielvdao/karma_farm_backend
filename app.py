from algo import KarmaRanker

import praw
from flask import Flask, session, request, jsonify, Response
from utils import *
import json



r = praw.Reddit(user_agent='karma_farm')
app = Flask(__name__)
app.debug = True
current_api_version = '/api/v0'

"""
Returns information about a user
"""
@app.route(current_api_version + '/user_profile/<username>', methods=['GET'])
def karam_histogram(username):
    user = r.get_redditor(username)
    user_json = {
        '_id' : str(username),
        'comment_karma' : user.comment_karma,
        'link_karma' : user.link_karma
    }

    return Response(json.dumps(user_json), mimetype='application/json')

"""
Returns a JSON list of top page submissions ranked from greatest to least for a certain subreddit
Limited to only 200 submissions as of current
"""
@app.route(current_api_version + '/top_page_submissions/<subreddit>', methods=['GET'])
def top_page_submissions(subreddit):
    submission_list = r.get_subreddit(subreddit).get_top(limit=200)
    result = []

    for submission in submission_list:
        item = {
            '_id' : get_link_id(submission.permalink),
            'title' : submission.title,
            'karma' : submission.score,
            'link' : 'http://redd.it/' + get_link_id(submission.permalink)
        }

        result.append(item)

    return Response(json.dumps(result), mimetype='application/json')

@app.route(current_api_version + 'algotest/<submission_id>')
def algo_test(submission_id):
    submission = r.get_submission(submission_id=submission_id)

    ranked_submission = KarmaRanker(submission.comments)
    return Response(ranked_submission.result, mimetype='application/json')


if __name__ == '__main__':
     app.run('0.0.0.0', port=5000)
