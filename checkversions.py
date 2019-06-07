import sys
import re

numpy_version_env = sys.argv[1]
scipy_version_env = sys.argv[2]
sklearn_version_env = sys.argv[3]
mpl_version_env = sys.argv[4]

numpy_regex = numpy_version_env.replace('.', r'\.')
scipy_regex = scipy_version_env.replace('.', r'\.')
sklearn_regex = sklearn_version_env.replace('.', r'\.')
mpl_regex = mpl_version_env.replace('.', r'\.')

numpy_pattern = re.compile(numpy_regex)
scipy_pattern = re.compile(scipy_regex)
sklearn_pattern = re.compile(sklearn_regex)
mpl_pattern = re.compile(mpl_regex)

import numpy
import scipy
import sklearn
import matplotlib as mpl

def match_entire_string(pattern, string):
  """
  Return True if pattern matches the entire string, False otherwise.
  """
  match = pattern.match(string)
  if match:
    return string == match.group(0)  # match.group(0) returns whole string
  else:
    return False

bool1 = match_entire_string(numpy_pattern, numpy.__version__)
bool2 = match_entire_string(scipy_pattern, scipy.__version__)
bool3 = match_entire_string(sklearn_pattern, sklearn.__version__)
bool4 = match_entire_string(mpl_pattern, mpl.__version__)
if bool1 and bool2 and bool3 and bool4:
  print('All versions look correct.')
else:
  sys.exit(1)