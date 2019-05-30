#   Copyright 2019 Vicram Rajagopalan
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

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
    np.random.seed(hash('test_nop_norm'))
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
