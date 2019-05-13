"""Functions to help create plots.
"""

from matplotlib.colors import Normalize
from skimage.transform import resize  # TODO get rid of skimage dependency

from misc import IS_TEST
from misc import printif
from misc import (DEBUGLVL, USERLVL)

NOP_NORM = Normalize(0.0, 1.0)
"""Instance of Normalize which is a no-op.

Normally, to assign colors to values in the consensus matrix,
matplotlib would rescale (normalize) the values in the matrix to be in
[0,1], but that's not the desired behavior. We would like the values to
simply be treated as values in [0,1] without modification, even if the
actual minimum value is higher than 0 or the actual max is less than 1.
The way to ensure that no normalization will be done is to provide our
own Normalizer and make it a no-op. 
"""


def _get_ax_size(ax, fig):
    """Find the size of an Axes, in pixels.

    Given an Axes and its parent Figure, this function will approximate
    the width and height of the Axes and return them in units of
    pixels. The code for this function was taken from `this
    stackoverflow post
    <https://stackoverflow.com/questions/19306510/determine-matplotlib-axis-size-in-pixels>`_.

    Parameters
    ----------
    ax : Axes
        The Axes for which you want to compute the dimensions. This may
        be part of a subplot.

    fig : Figure
        The Figure which contains ax.

    Returns
    -------
    width : int
        The approximate width of ax, rounded to the nearest pixel.

    height : int
        The approximate height of ax, rounded to the nearest pixel.
    """
    bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    width, height = bbox.width, bbox.height
    width *= fig.dpi
    height *= fig.dpi
    return (width, height)


def plot_consensus_heatmap(ordered_cmat, ax, fig, cmap, downsample, verbose):
    """Plot the given consensus matrix as a heatmap.

    This function plots the consensus heatmap onto the given Axes. The
    consensus matrix must have already been reordered to group samples
    in each cluster together. This is required to get the "block
    matrix" look.

    To actually plot the heatmap, this function will call
    matplotlib.axes.Axes.imshow. imshow has some potential memory
    issues; see `this stackoverflow post
    <https://stackoverflow.com/questions/9525706/excessive-memory-usage-in-matplotlib-imshow>`_.
    This is likely caused by imshow storing the entire matrix and doing
    computations on it at plotting-time. To deal with this, we can
    downsample the consensus matrix before passing it to imshow. This
    just involves creating a smaller matrix that would look about the
    same if plot, then plotting the smaller matrix.

    Parameters
    ----------
    ordered_cmat : ndarray
        This is the consensus matrix to plot. Must be a symmetric
        2-dimensional ndarray with values between 0 and 1. The values
        should have been reordered to group samples in the same cluster
        together.

    ax : Axes
        The matplotlib Axes object onto which the heatmap will be
        drawn.

    fig : Figure
        Must be the matplotlib Figure object which contains ax. It
        will not be mutated; this function will only be reading some of
        its attributes.

    cmap : str or Colormap
        This param determines the colormap which will be used to draw
        the heatmap. It can be anything which can be passed to the
        'cmap' param of imshow. Usually this will be a string which
        corresponds to the name of a colormap. For names of matplotlib
        colormaps, as well as recommendations for their usage, see
        `this tutorial
        <https://matplotlib.org/tutorials/colors/colormaps.html>`_.

    downsample: boolean
        Determines whether the consensus matrix will be downsampled
        before it is passed to imshow.

    verbose: non-negative int
        Verbosity level of print statements. If this is 0, no output
        will be produced. If >= 1, some print statements will trigger.
    """
    printif(
        verbose >= DEBUGLVL,
        'Entering plot_consensus_heatmap'
    )
    # TODO input checking
    if IS_TEST:
        # check ndarray
        # check 2d
        # check values in [0,1]
        # check symmetric
        pass
