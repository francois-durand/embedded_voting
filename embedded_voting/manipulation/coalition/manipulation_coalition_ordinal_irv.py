import numpy as np
from embedded_voting.embeddings.embeddings_generator_polarized import EmbeddingsGeneratorPolarized
from embedded_voting.manipulation.coalition.manipulation_coalition_ordinal import ManipulationCoalitionOrdinal
from embedded_voting.ratings_from_embeddings.ratings_from_embeddings_correlated import RatingsFromEmbeddingsCorrelated
from embedded_voting.scoring.singlewinner.rule_instant_runoff_extension import RuleInstantRunoffExtension
from embedded_voting.scoring.singlewinner.rule_svd_nash import RuleSVDNash


class ManipulationCoalitionOrdinalIRV(ManipulationCoalitionOrdinal):
    """
    This class do the coalition manipulation
    analysis for the :class:`RuleInstantRunoffExtension` extension.

    Parameters
    ----------
    ratings: Ratings or np.ndarray
        The ratings of voters to candidates
    embeddings: Embeddings
        The embeddings of the voters
    rule : Rule
        The aggregation rule we want to analysis.

    Examples
    --------
    >>> np.random.seed(42)
    >>> ratings_dim_candidate = [[1, .2, 0], [.5, .6, .9], [.1, .8, .3]]
    >>> embeddings = EmbeddingsGeneratorPolarized(10, 3)(.8)
    >>> ratings = RatingsFromEmbeddingsCorrelated(coherence=0.8, ratings_dim_candidate=ratings_dim_candidate)(embeddings)
    >>> manipulation = ManipulationCoalitionOrdinalIRV(ratings, embeddings, RuleSVDNash())
    >>> manipulation.winner_
    2
    >>> manipulation.is_manipulable_
    True
    >>> manipulation.worst_welfare_
    0.0
    """

    def __init__(self, ratings, embeddings, rule=None):
        if not isinstance(ratings, np.ndarray):
            ratings = ratings.ratings
        super().__init__(ratings, embeddings, extension=RuleInstantRunoffExtension(ratings.shape[1]), rule=rule)
