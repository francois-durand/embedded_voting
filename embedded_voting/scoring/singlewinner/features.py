# -*- coding: utf-8 -*-
"""
Copyright Théo Delemazure
theo.delemazure@ens.fr

This file is part of Embedded Voting.
"""
import numpy as np
from embedded_voting.utils.cached import cached_property
from embedded_voting.utils.miscellaneous import normalize
from embedded_voting.scoring.singlewinner.general import ScoringRule
from embedded_voting.profile.profile import Profile
from embedded_voting.embeddings.embeddings import Embeddings
import matplotlib.pyplot as plt


class FeaturesRule(ScoringRule):
    """
    Voting rule in which the aggregated score of
    a candidate is the norm of the feature
    vector of this candidate.

    Parameters
    ----------
    profile : Profile
        The profile of voters on which we run the election.

    Examples
    --------
    >>> scores = np.array([[.5, .6, .3], [.7, 0, .2], [.2, 1, .8]])
    >>> embeddings = np.array([[1, 1], [1, 0], [0, 1]])
    >>> profile = Profile(scores, Embeddings(embeddings).normalize())
    >>> election = FeaturesRule(profile)
    >>> election.scores_
    [0.44784902576697316, 0.9271320343559639, 0.43356601717798204]
    >>> election.ranking_
    [1, 0, 2]
    >>> election.winner_
    1
    >>> election.welfare_
    [0.028938395456510148, 1.0, 0.0]
    """

    @cached_property
    def features_(self):
        """
        This function return the
        feature vector of all candidates.

        Return
        ------
        np.ndarray
            The matrix of features.
            Its shape is :attr:`~embedded_voting.Profile.n_candidates`, :attr:`~embedded_voting.Profile.n_dim`
        """
        positions = self.profile_.embeddings.positions
        ratings = self.profile_.ratings
        return np.dot(np.dot(np.linalg.pinv(np.dot(positions.T, positions)), positions.T), ratings).T

    def _score_(self, candidate):
        return (self.features_[candidate] ** 2).sum()

    def plot_features(self, plot_kind="3D", dim=None, row_size=5, show=True):
        """
        This function plot the features vector of
        all candidates in the given dimensions.

        Parameters
        ----------
        plot_kind : str
            The kind of plot we want to show.
            Can be ``'3D'`` or ``'ternary'``.
        dim : list
            The 3 dimensions we are using for our plot.
            By default, it is set to ``[0, 1, 2]``.
        row_size : int
            The number of subplots by row.
            By default, it is set to 5 plots by row.
        show : bool
            If True, plot the figure
            at the end of the function.
        """
        if dim is None:
            dim = [0, 1, 2]
        else:
            if len(dim) != 3:
                raise ValueError("The number of dimensions should be 3")

        n_candidate = self.profile_.n_candidates
        n_rows = (n_candidate - 1) // row_size + 1
        fig = plt.figure(figsize=(row_size * 5, n_rows * 5))
        plot_position = [n_rows, row_size, 1]
        features = self.features_
        for candidate in range(n_candidate):
            ax = self.profile_.plot_candidate(candidate,
                                              plot_kind=plot_kind,
                                              dim=dim,
                                              fig=fig,
                                              plot_position=plot_position,
                                              show=False)
            if plot_kind == "3D":
                x1 = features[candidate, dim[0]]
                x2 = features[candidate, dim[1]]
                x3 = features[candidate, dim[2]]
                ax.plot([0, x1], [0, x2], [0, x3], color='k', linewidth=2)
                ax.scatter([x1], [x2], [x3], color='k', s=5)
            elif plot_kind == "ternary":
                x1 = features[candidate, dim[0]]
                x2 = features[candidate, dim[2]]
                x3 = features[candidate, dim[1]]
                feature_bis = [x1, x2, x3]
                feature_bis = np.maximum(feature_bis, 0)
                size_features = np.linalg.norm(feature_bis)
                feature_bis = normalize(feature_bis)
                ax.scatter([feature_bis ** 2], color='k', s=50*size_features+1)
            plot_position[2] += 1

        if show:
            plt.show()  # pragma: no cover
