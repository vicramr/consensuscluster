"""Contains unit tests to be run with pytest."""

import pytest
from matplotlib.figure import Figure
from matplotlib import pyplot as plt

from consensuscluster.plotutils import _get_ax_size


# *** BEGIN helper objects/tests for _get_ax_size ***
MAX_ERROR = .1  # We're willing to tolerate at most 10% error


def _check_answer(true_width_pix, true_height_pix,
                 approx_width_pix, approx_height_pix):
    """Helper function for testing _get_ax_size.

    Asserts that the answer found by _get_ax_size is within the
    acceptable margin of error of the true answer (or at least,
    whatever we're considering the true answer to be).
    :param true_width_pix: True width of the Axes, in pixels.
    :param true_height_pix: True height of the Axes, in pixels.
    :param approx_width_pix: The width approximation returned by
    _get_ax_size.
    :param approx_height_pix: The height approximation returned by
    _get_ax_size.
    :return: nothing.
    """
    width_lower_bound = true_width_pix - MAX_ERROR * true_width_pix
    width_upper_bound = true_width_pix + MAX_ERROR * true_width_pix
    height_lower_bound = true_height_pix - MAX_ERROR * true_height_pix
    height_upper_bound = true_height_pix + MAX_ERROR * true_height_pix

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


def test_get_ax_size():
    """
    Tests that _get_ax_size returns an answer that is within a
    reasonable margin of the answer you'd get by hand.

    Because I just grabbed this function off of stackoverflow without
    any evidence that it was actually correct, it's important to really
    test the bejesus out of it.
    :return: nothing.
    """

    for figsize in figsizes:
        (width, height) = figsize  # True values, in inches
        for dpi in dpis:
            # True values, in pixels
            width_pix = width * dpi
            height_pix = height * dpi

            # First: try figure.Figure
            fig1 = Figure(figsize=figsize, dpi=dpi)
            ax1 = fig1.gca()
            # ax1 should cover the entire figure.
            (approx_width_1, approx_height_1) = _get_ax_size(ax1, fig1)
            _check_answer(width_pix, height_pix,
                         approx_width_1, approx_height_1)

            # Second, create a subplot on that same Figure
            axarr1 = fig1.subplots(5, 3)
            correct_width_sub = width_pix / 3
            correct_height_sub = height_pix / 5
            for i in range(5):
                for j in range(3):
                    ax_sub = axarr1[i, j]
                    (approx_width_sub, approx_height_sub) = _get_ax_size(
                        ax_sub,
                        fig1
                    )
                    _check_answer(correct_width_sub, correct_height_sub,
                                 approx_width_sub, approx_height_sub)

# *** END helper objects/tests for _get_ax_size ***
