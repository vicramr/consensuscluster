"""Contains unit tests."""
import random

import pytest
import numpy as np

from consensuscluster.tests.conftest import small_cmats, set_random_seeds
from consensuscluster.plotutils import NOP_NORM
from consensuscluster.misc import assert_is_consensus_matrix


@pytest.mark.parametrize(
    'input_factory',
    [
        lambda: 0,
        lambda: 1,
        lambda: 0.0,
        lambda: 1.0,
        lambda: .99,
        lambda: .5,
        lambda: .00001,
        lambda: np.zeros((5, 90)),
        lambda: np.zeros(77, np.float32),
        lambda: np.zeros(55) + .3,
        lambda: np.ones((4, 5, 6, 7), np.int8) - .0001,
        lambda: np.random.random_sample((100, 101, 5)),
        lambda: np.random.random_sample((80, 80))
    ]
)
def test_nop_norm(input_factory):
    """Tests that NOP_NORM is indeed a no-op.

    NOP_NORM is a matplotlib Normalize object. These are callables
    which can take scalars or ndarrays as input. We need to test that
    for any input values in [0,1], NOP_NORM is the identity function.
    That is, the output should be equivalent to the input. (Or at
    least very close, due to floating-point arithmetic.)


    The parameterization for this function is a bit involved. Here's
    what's going on: we want to test NOP_NORM with lots of different
    cases of scalars and ndarrays, including inputs with lots of random
    values between 0 and 1. However, we also want to ensure
    reproducibility by setting a random seed. A relatively-clean
    solution is to make the input parameters be factory functions,
    rather than just the inputs themselves. That way, we can set the
    random seed once at the beginning of this function, then call the
    factory function to get the input after the seed is set.
    """

    # Note: Judging from the source code of the Normalize class, it
    # should also do nothing even for values outside of [0,1], but
    # we're not interested in testing this case.
    set_random_seeds('test_nop_norm', input_factory)
    val = input_factory()
    norm_val = NOP_NORM(val)
    # There is some floating-point arithmetic occurring in the above
    # line. According to the source code for the Normalize class,
    # each value in the input will have 0.0 subtracted from it, then
    # will be divided by (1.0 - 0.0).
    # To my knowledge, even this small number of floating-point
    # operations could introduce precision errors, so we need to do
    # a floating-point comparison with np.allclose rather than using
    # something like np.array_equal.
    assert np.allclose(val, norm_val)
    # According to the numpy docs, np.allclose is NOT commutative, so
    # to be extra sure, we'll check both here.
    assert np.allclose(norm_val, val)


@pytest.mark.parametrize('cmat', small_cmats)
def test_sample_consensus_matrices(cmat):
    """Test that the arrays in small_cmats pass as consensus matrices

    This test uses assert_is_consensus_matrix on the consensus
    matrices in small_cmats. All of these should be well-formed.
    """
    assert_is_consensus_matrix(cmat)


def test_set_random_seeds():
    """Test that set_random_seeds actually ensures reproducibility."""
    lst1 = []
    lst2 = []
    lst3 = []
    lst4 = []
    for _ in range(20):
        set_random_seeds('test_set_random_seeds', 1, 3.14, ('this', 'is', 'a', 'tuple'))
        lst1.append(random.random())
        lst2.append(np.random.rand(6, 7, 8))
        lst3.append(random.sample(['foo', 'bar', 'baz', 'quux'], 3))
        lst4.append(np.random.gamma(5.67, 9.9999, size=(10, 11, 2)))
    for elem1 in lst1:
        for elem2 in lst1:
            assert elem1 == elem2
    for elem1 in lst2:
        for elem2 in lst2:
            assert np.array_equal(elem1, elem2)
    for elem1 in lst3:
        for elem2 in lst3:
            assert elem1 == elem2
    for elem1 in lst4:
        for elem2 in lst4:
            assert np.array_equal(elem1, elem2)
