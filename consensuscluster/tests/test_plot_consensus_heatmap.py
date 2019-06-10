"""Tests for plotutils.plot_consensus_heatmap"""

import pytest
import numpy as np
from matplotlib.testing import decorators

from consensuscluster.tests.conftest import small_cmats, set_random_seeds
from consensuscluster.plotutils import plot_consensus_heatmap
