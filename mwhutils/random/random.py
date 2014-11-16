"""
Sample from low-discrepancy sequences.
"""

# future imports
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

# local imports
from ._sobol import i4_sobol_generate

# global imports
import numpy as np

# exported symbols
__all__ = ['rstate', 'uniform', 'latin', 'sobol']


def rstate(rng=None):
    """
    Return a numpy RandomState object. If an integer value is given then a new
    RandomState will be returned with this seed. If None is given then the
    global numpy state will be returned. If an already instantiated state is
    given this will be passed back.
    """
    if rng is None:
        return np.random.mtrand._rand
    elif isinstance(rng, np.random.RandomState):
        return rng
    elif isinstance(rng, int):
        return np.random.RandomState(rng)
    raise ValueError('unknown seed given to rstate')


def uniform(bounds, n, rng=None):
    """
    Sample n points uniformly at random from the specified region, given by
    a list of [(lo,hi), ..] bounds in each dimension.
    """
    # if given a seed or an instantiated RandomState make sure that we use
    # it here, but also within the sample_spectrum code.
    rng = rstate(rng)
    bounds = np.array(bounds, ndmin=2, copy=False)

    # generate the random values.
    d = len(bounds)
    w = bounds[:, 1] - bounds[:, 0]
    X = bounds[:, 0] + w * rng.rand(n, d)

    return X


def latin(bounds, n, rng=None):
    """
    Sample n points from a latin hypercube within the specified region, given
    by a list of [(lo,hi), ..] bounds in each dimension.
    """
    rng = rstate(rng)
    bounds = np.array(bounds, ndmin=2, copy=False)

    # generate the random samples.
    d = len(bounds)
    w = bounds[:, 1] - bounds[:, 0]
    X = bounds[:, 0] + w * (np.arange(n)[:, None] + rng.rand(n, d)) / n

    # shuffle each dimension.
    for i in xrange(d):
        X[:, i] = rng.permutation(X[:, i])

    return X


def sobol(bounds, n, rng=None):
    """
    Sample n points from a sobol sequence within the specified region, given by
    a list of [(lo,hi), ..] bounds in each dimension.
    """
    rng = rstate(rng)
    bounds = np.array(bounds, ndmin=2, copy=False)

    # generate the random samples.
    d = len(bounds)
    skip = rng.randint(100, 200)
    w = bounds[:, 1] - bounds[:, 0]
    X = bounds[:, 0] + w * i4_sobol_generate(d, n, skip).T

    return X
