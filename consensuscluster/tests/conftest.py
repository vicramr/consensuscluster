"""This file contains global configurations for pytest.

See here for some reasoning as to why we put the conftest file here:
https://docs.pytest.org/en/2.7.3/plugins.html#conftest-py-local-per-directory-plugins
Specifically: "If you have conftest.py files which do not reside in a
python package directory (i.e. one containing an __init__.py) then
“import conftest” can be ambiguous because there might be other
conftest.py files as well on your PYTHONPATH or sys.path. It is thus
good practise for projects to either put conftest.py under a package
scope or to never import anything from a conftest.py file."
"""
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
              [.00000054001, .003, 0.0, 1.0]])
]
