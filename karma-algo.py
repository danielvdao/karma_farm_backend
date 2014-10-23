"""
Alien - The Ranking algorithm for KarmaFarm
Excepts a list of PRAW comment objects (forest)
Returns JSON for display by Android
"""
from flask import jsonify
import json


class KarmaRanker:
  def __init__(self, forest):
    self.forest = forest

    result = []

    for comment in forest:
      pass

    return json.dumps(result)
