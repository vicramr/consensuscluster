"""This file contains global configs & utilities for pytest.

See here for some reasoning as to why we put the conftest file here:
https://docs.pytest.org/en/2.7.3/plugins.html#conftest-py-local-per-directory-plugins
Specifically: "If you have conftest.py files which do not reside in a
python package directory (i.e. one containing an __init__.py) then
“import conftest” can be ambiguous because there might be other
conftest.py files as well on your PYTHONPATH or sys.path. It is thus
good practise for projects to either put conftest.py under a package
scope or to never import anything from a conftest.py file."
"""
import random

import numpy as np

# The next 2 functions allow us to detect, at runtime, whether a test
# is being run. See:
# https://docs.pytest.org/en/latest/example/simple.html#detect-if-running-from-within-a-pytest-run


def pytest_configure(config):
    import sys

    sys._called_from_test = True


def pytest_unconfigure(config):
    import sys

    del sys._called_from_test


# This is a list of consensus matrices that will be used for testing
# functions that take a consensus matrix as input.
cmat_list = [
    np.array([[1.0, 1.0],
              [1.0, 1.0]],
             dtype=np.float32),
    np.array([[1.0, 0.0, 0.5],
              [0.0, 1.0, 0.27],
              [0.5, 0.27, 1.0]]),
    np.array([[1.0, .998, .3874, .00000054001],
              [.998, 1.0, .7523, 0.0],
              [.3874, .7523, 1.0, .003],
              [.00000054001, 0.0, .003, 1.0]])
]


def set_random_seeds(id_string, *args):
    """Set unique Python and numpy random seeds for the given inputs.

    This function uses hashing to generate two random seeds from the
    given inputs. These seeds will almost certainly be different from
    each other and also from any other random seeds returned for
    different inputs. Effectively, the inputs are combined together
    into a single hash key.

    The motivation for this function is as follows: we want our tests
    to be reproducible, which involves setting constant random seeds
    in every test that uses a random number generator. But we also want
    to avoid bias in the tests, which could be introduced by using the
    same random seeds in every test. One solution might be to manually
    choose different hard-coded seeds for every test, but this is
    cumbersome and error-prone. A better way would be to
    programmatically generate unique random seeds for each test.
    That is what this function is for.

    :param id_string: Should be a string that uniquely identifies
    the test that's calling this function. In practice, this means
    that you should always pass the name of the test for this input.

    :param args: Any other objects that you want to use to construct
    a hash key. In practice, for parametrized tests, args should be
    the parameters. All args passed MUST be hashable.

    :return: Nothing.
    """
    # First set the Python random seed.
    # Here, we create a tuple out of the params. Python is smart about
    # combining the hash codes of elements in a tuple into a new hash
    # code.
    hash_key_1 = tuple([id_string, *args])
    random.seed(hash(hash_key_1))

    # Next, set the Numpy random seed after perturbing the string
    # slightly to ensure the hash code will be different.
    new_id_string = id_string + 'foo'
    hash_key_2 = tuple([new_id_string, *args])
    # numpy.random.seed requires the seed to be 32-bit.
    seed = hash(hash_key_2) % (1 << 32)
    np.random.seed(seed)
