
import json
import praw

class KarmaRanker:
  """
  The Ranking algorithm class for KarmaFarm
  """

  DEPTH_FACTOR = 0.3  # scales depth value
  KARMA_FACTOR = 0.3  # scales current karma of comment
  REPLY_FACTOR = 0.3  # scales number of immediate replies

  def __init__(self, forest):
    self.forest = forest
    self.total_karma = self.get_total_karma(self.forest)
    self.result = rank()

  def rank(self):
    """
    recursively traverse comment tree (depth-first) calculating
    karma potential score 'rank' for each comment
    """
    depth = 0

    comment_json = self.rank_helper(self.forest, depth, result=[])

    return json.dumps(comment_json)


  def rank_helper(self, forest, depth, result=NULL):
    
    if forest and not issubclass(praw.objects.MoreComments, forest):
      depth += 1
      comment_json = []

      for comment in forest:
        comment_data = {
          'body': comment.body,
          'score': comment.score,
          'rank': calculate_rank(comment.score, len(comment.replies), depth),
          'link': comment.permalink,
          'replies': rank_helper(comment.replies, depth, comment_json)
        }
        comment_json.append(comment_data)

      result.append(comment_json)
      return result

  def calculate_rank(score, num_replies, depth):
    """
    formula for karma potential ranking
    """
    return 1000 - (score * KARMA_FACTOR)
                - (num_replies * REPLY_FACTOR)
                - (depth * DEPTH_FACTOR)


  def print_result(self):
    print self.result

  @classmethod
  def get_total_karma(forest):
      return sum([comment.score for comment in  praw.helpers.flatten_tree(forest)])
