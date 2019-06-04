"""Miscellaneous things.
"""

import numpy as np
from scipy.sparse import issparse

import sys
# We're using pytest to run tests. It's set up so that when tests are
# being run, pytest will set the attribute '_called_from_test' on the
# sys module. This means we can tell whether we're inside a testing
# session by checking whether this attribute exists. IS_TEST is a
# global boolean variable that denotes whether we're in a pytest run.
# Pytest documentation:
# https://docs.pytest.org/en/latest/example/simple.html#detect-if-running-from-within-a-pytest-run
IS_TEST = False
if hasattr(sys, '_called_from_test'):
    IS_TEST = True


def printif(condition, *args, **kwargs):
    """Wrapper function for print. Only prints if condition is met.

    condition will be treated as a boolean. If it is True, the rest of
    the parameters will be forwarded to print.
    Usually, condition will be "verbose >= some value".
    """
    if condition:
        print(*args, **kwargs)


# Below are global constants for verbosity levels.

DEBUGLVL = 4
"""Very verbose output, mainly for use when debugging/testing."""

USERLVL = 1
"""User-level verbosity: less verbose, intended for the end user."""


def assert_is_consensus_matrix(mat):
    """Asserts that mat is a valid consensus matrix.

    Returns nothing. If mat violates any of the criteria for being a
    consensus matrix, this function will raise an AssertionError.

    Note: it is possible that a matrix could pass these checks even
    though it could not possibly be produced from a correct run of
    consensus clustering. This function only checks the structural
    aspects which are easiest to verify.
    """
    # We want to check that mat is:
    # * a dense ndarray
    # * 2D
    # * square
    # * in [0,1]
    # * symmetric
    assert isinstance(mat, np.ndarray)
    assert not issparse(mat)
    assert mat.ndim == 2
    assert mat.shape[0] == mat.shape[1]
    assert np.all(
        np.logical_and(
            mat >= 0.0,
            mat <= 1.0
        )
    )
    # Check that mat is symmetric.
    # rtol is set to 0 here because we have such a small range of
    # values (between 0 and 1) that it won't make much of a difference.
    # So this just checks that all values are within 1e-7.
    # That's easy to understand and also commutative (with nonzero
    # rtol, np.allclose is not commutative)
    assert np.allclose(mat, mat.T, rtol=0.0, atol=1e-7)
    # Check that the elements on the diagonals are all 1s
    diag = np.diagonal(mat)
    ones = np.ones_like(diag)
    assert np.allclose(diag, ones, rtol=0.0, atol=1e-8)
