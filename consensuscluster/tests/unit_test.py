"""Contains unit tests."""

import pytest
import numpy as np

from consensuscluster.plotutils import NOP_NORM


def test_nop_norm():
    """
    Tests that NOP_NORM is indeed a no-op.
    :return: nothing
    """
    # matplotlib Normalize objects can take scalars or ndarrays as
    # input. We need to test that for any input values [0,1], NOP_NORM
    # does nothing.
    # Judging from the source code of the Normalize class, it should
    # also do nothing even for values outside of this interval, but
    # we're not interested in testing this case.
    np.random.seed(4)
    test_cases = [
        0,
        1,
        0.0,
        1.0,
        .99,
        .5,
        .00001,
        np.zeros((5, 90)),
        np.zeros(77, np.float32),
        np.zeros(55) + .3,
        np.ones((4, 5, 6, 7), np.int8) - .0001,
        np.random.random_sample((100, 101, 5)),
        np.random.random_sample((80, 80))
    ]

    for val in test_cases:
        norm_val = NOP_NORM(val)
        assert np.allclose(val, norm_val)
        # According to the numpy docs, np.allclose is NOT symmetric, so
        # to be extra sure, we'll check both here.
        assert np.allclose(norm_val, val)
