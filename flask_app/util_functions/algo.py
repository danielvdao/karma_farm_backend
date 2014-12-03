
import json
import praw
import utils

class KarmaRanker:
    """
    The Ranking algorithm class for KarmaFarm
    """

    DEPTH_FACTOR = 45  # scales depth value
    KARMA_FACTOR = 150  # scales current karma of comment
    REPLY_FACTOR = 30  # scales number of immediate replies

    def __init__(self, forest):
        self.forest = forest
        self.total_karma = self.get_total_karma(self.forest)
        self.total_comments = 0
        self.rank()

    def rank(self):
        """
        create json list of ranked comments for a given submission forest
        """
        depth = 0

        comment_json = {'comments': []}
        self.rank_helper(self.forest, depth, comment_json['comments'])

        comment_json['total_karma'] = len(self.forest)
        comment_json['total_comments'] = self.total_comments

        self.result = json.dumps(comment_json)


    def rank_helper(self, forest, depth, result):
        """
        recursively traverse comment tree (depth-first) calculating
        karma potential score 'rank' for each comment
        """
        if forest:
            comment_json = []
            self.total_comments += len(forest)

            for comment in forest:


                if issubclass(praw.objects.Comment, comment.__class__):


                    rank = self.calculate_rank(comment.score,          \
                                               len(comment.replies),   \
                                               depth)                  \

                    comment_data = {
                        'text': comment.body,
                        'score': comment.score,
			'author': str(comment.author),
                        'link': comment.permalink,
                        # need a subtree size method if we want
                        # to look at sub levels
                        'rank': rank,
                        '_id': comment.id
                    }

                    if comment.replies:

                        replies = self.rank_helper(comment.replies,    \
                                                   depth + 1,          \
                                                   result=[])
                        comment_data['replies'] = replies


                elif issubclass(praw.objects.MoreComments, comment.__class__):
                    # not supporting MoreCommentsObjects in beta
                    pass
                else:
                    raise TypeError("unexpected comment object for ranking")

                comment_json.append(comment_data)

            result.append(comment_json)
            return result
        else:
            return None

    def calculate_rank(self, score, num_replies, depth):
        """
        formula for karma potential ranking
        """
        return 500  + ((score / self.total_karma) * KarmaRanker.KARMA_FACTOR)        \
                    - (num_replies * KarmaRanker.REPLY_FACTOR)  \
                    - (depth * KarmaRanker.DEPTH_FACTOR)        \

    def get_total_karma(self, forest):
        """
        return sum of all comment scores in reacheable comments
        """
        return sum([comment.score for comment in praw.helpers.flatten_tree(forest) \
                if issubclass(praw.objects.Comment, comment.__class__)])
