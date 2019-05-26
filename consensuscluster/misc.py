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

"""Miscellaneous things.
"""


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
