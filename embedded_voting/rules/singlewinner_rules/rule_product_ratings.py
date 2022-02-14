import numpy as np
from embedded_voting.rules.singlewinner_rules.rule import Rule
from embedded_voting.ratings.ratings import Ratings


class RuleProductRatings(Rule):
    """
    Voting rule in which the score of a candidate is the product of her ratings.

    More precisely, her score is a tuple whose components are:

    * The number of her nonzero ratings.
    * The product of her nonzero ratings.

    Note that this rule is well suited only if ratings are nonnegative.

    No embeddings are used for this rule.

    Examples
    --------
    >>> ratings = Ratings(np.array([[.5, .6, .3], [.7, 0, .2], [.2, 1, .8]]))
    >>> election = RuleProductRatings()(ratings)
    >>> election.scores_
    [(3, 0.06999999999999999), (2, 0.6), (3, 0.048)]
    >>> election.ranking_
    [0, 2, 1]
    >>> election.winner_
    0
    >>> election.welfare_
    [1.0, 0.0, 0.6857142857142858]
    """

    def __init__(self, embeddings_from_ratings=None):
        super().__init__(score_components=2, embeddings_from_ratings=embeddings_from_ratings)

    def _score_(self, candidate):
        candidate_ratings = self.ratings_.candidate_ratings(candidate)
        mask = candidate_ratings > 0
        n_nonzero_ratings = np.sum(mask)
        prod_nonzero_ratings = np.prod(candidate_ratings[mask])
        return n_nonzero_ratings, prod_nonzero_ratings
