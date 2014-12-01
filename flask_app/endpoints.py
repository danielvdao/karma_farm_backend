#!/root/karma_farm_backend/venv/bin/python
from flask import Flask, request, Response

import praw 
import json 

from util_functions import KarmaRanker
from util_functions import get_link_id

from flask_app import app


r = praw.Reddit(user_agent='karma_farm')
current_api_version = '/api/v0'

"""
Returns information about a user
"""
@app.route(current_api_version + '/user_profile/<username>', methods=['GET'])
def karma_histogram(username):
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
        _id = get_link_id(submission.short_link)

        item = {
            'permalink': submission.permalink,
            '_id' : _id,
            'title' : submission.title,
            'karma' : submission.score,
        }

        result.append(item)

    return Response(json.dumps(result), mimetype='application/json')

"""
Returns JSON payload for ranking algorithm testing
"""
@app.route(current_api_version + '/comments/<submission_id>', methods=['GET'])
def algo_test(submission_id):
    submission = r.get_submission(submission_id=submission_id)
    ranked_submission = KarmaRanker(submission.comments)
    return Response(ranked_submission.result, mimetype='application/json')

"""
Logs in and comments
"""
@app.route(current_api_version + '/login/comment', methods=['POST'])
def post():
    content = request.get_json(force=True)
   
    result = False
    if content is not None:
        result = True
    data = {
            'success' : result     
    }
    return Response(json.dumps(data), mimetype='application/json')

