"""Contains unit tests to be run with pytest."""

import pytest
from matplotlib.figure import Figure
from matplotlib import pyplot as plt

from consensuscluster.plotutils import _get_ax_size

def test_get_ax_size():
    """
    Tests that _get_ax_size returns an answer that is within a
    reasonable margin of the answer you'd get by hand.

    Because I just grabbed this function off of stackoverflow without
    any evidence that it was actually correct, it's important to really
    test the bejesus out of this function.
    :return: nothing.
    """
    max_error = .1  # We're willing to tolerate at most 10% error

    def check_answer(true_width_pix, true_height_pix,
                     approx_width_pix, approx_height_pix):
        width_lower_bound = true_width_pix - max_error * true_width_pix
        width_upper_bound = true_width_pix + max_error * true_width_pix
        height_lower_bound = true_height_pix - max_error * true_height_pix
        height_upper_bound = true_height_pix + max_error * true_height_pix

        assert width_lower_bound <= approx_width_pix <= width_upper_bound
        assert height_lower_bound <= approx_height_pix <= height_upper_bound

    figsizes = [
        (1, 1),
        (3, 3),
        (4, 4),
        (4, 9),
        (.87, .4445),
        (5.829, 1)
    ]
    dpis = [100, 43.793]

    for figsize in figsizes:
        (width, height) = figsize  # True values, in inches
        for dpi in dpis:
            width_pix = width * dpi  # True value, in pixels
            height_pix = height * dpi

            # First: try figure.Figure
            fig1 = Figure(figsize=figsize, dpi=dpi)
            ax1 = fig1.gca()
            # ax1 should cover the entire figure.
            (approx_width_1, approx_height_1) = _get_ax_size(ax1, fig1)
            check_answer(width_pix, height_pix,
                         approx_width_1, approx_height_1)


