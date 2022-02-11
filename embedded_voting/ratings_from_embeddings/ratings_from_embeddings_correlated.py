import numpy as np

from embedded_voting.ratings.ratings import Ratings
from embedded_voting.embeddings.embeddings import Embeddings
from embedded_voting.ratings_from_embeddings import RatingsFromEmbeddings
from embedded_voting.ratings.ratings_generator_uniform import RatingsGeneratorUniform


class RatingsFromEmbeddingsCorrelated(RatingsFromEmbeddings):
    """
    This method create ratings correlated to the embeddings by a score matrix.

    Parameters
    ----------
    coherence: float
        Between 0 and 1, indicates the desired level of correlation between embeddings and ratings. If 0,
        ratings are random, if 1, ratings are perfectly correlated to embeddings.
    ratings_dim_candidate: np.ndarray or list
        An array with shape ``n_dim, n_candidates`` such that ``ratings_dim_candidate[i,j]`` determines the rating
        given by the group of voter in the dimension i to candidate j. If none is specified, a random one
        is generated
    ratings_dim_candidate : np.ndarray or list
        Matrix of shape :attr:`n_dim`, :attr:`n_candidates` containing the scores given by
        each group. More precisely, `ratings_dim_candidate[i,j]` is the score given by the group
        represented by the dimension i to the candidate j.
        By default, it is set at random with a uniform distribution.
    n_dim: int
        The number of dimension of the embeddings
    n_candidates: int
        The number of candidates wanted in the ratings
    minimum_random_rating: float
        Minimum rating for the random part.
    maximum_random_rating: float
        Maximum rating for the random part.
    clip: bool
        If true, the final ratings are clipped in the interval [`minimum_random_rating`, `maximum_random_rating`].

    Examples
    --------
    >>> np.random.seed(42)
    >>> embeddings = Embeddings(np.array([[0, 1], [1, 0], [1, 1]]), norm=True)
    >>> generator = RatingsFromEmbeddingsCorrelated(coherence=.5, ratings_dim_candidate=np.array([[.8,.4],[.1,.7]]))
    >>> generator(embeddings)
    Ratings([[0.23727006, 0.82535715],
             [0.76599697, 0.49932924],
             [0.30300932, 0.35299726]])
    """

    def __init__(self, coherence=0, ratings_dim_candidate=None, n_dim=None, n_candidates=None,
                 minimum_random_rating=0, maximum_random_rating=1, clip=False):
        if ratings_dim_candidate is None:
            ratings_dim_candidate = np.random.rand(n_dim, n_candidates)
        else:
            if n_dim is not None and n_dim != ratings_dim_candidate.shape[0]:
                raise ValueError("n_dim should be omitted or equal to ratings_dim_candidate.shape[0].")
            if n_candidates is not None and n_candidates != ratings_dim_candidate.shape[1]:
                raise ValueError("n_candidates should be omitted or equal to ratings_dim_candidate.shape[1].")
            ratings_dim_candidate = np.array(ratings_dim_candidate)
            n_dim, n_candidates = ratings_dim_candidate.shape
        # Store variables
        self.coherence = coherence
        self.ratings_dim_candidate = ratings_dim_candidate
        self.n_dim = n_dim
        self.minimum_random_rating = minimum_random_rating
        self.maximum_random_rating = maximum_random_rating
        self.clip = clip
        super().__init__(n_candidates)

    def __call__(self, embeddings, *args):
        """
        This method generate ratings from the embeddings using the score matrix.

        Parameters
        ----------
        embeddings: Embeddings
            The embeddings we want to use to obtain the ratings

        Return
        ------
        Ratings
        """
        embeddings = Embeddings(embeddings, norm=True)
        ratings_from_embeddings = embeddings ** 2 @ self.ratings_dim_candidate
        ratings_random = RatingsGeneratorUniform(
            n_voters=embeddings.n_voters,
            minimum_rating=self.minimum_random_rating,
            maximum_rating=self.maximum_random_rating
        )(self.n_candidates)
        ratings = self.coherence * ratings_from_embeddings + (1 - self.coherence) * ratings_random
        if self.clip:
            ratings = np.clip(ratings, self.minimum_random_rating, self.maximum_random_rating)
        return Ratings(ratings)
