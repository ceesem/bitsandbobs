import matplotlib
import seaborn as sns
import numpy as np
plt = matplotlib.pyplot

axis_label_font = {'family': 'sans-serif',
                   'weight': 'normal',
                   'size': 12,
                   }

axis_tick_font = {'family': 'sans-serif',
                  'weight': 'normal',
                  'size': 10,
                  }


def set_rc_params(mpl):
    mpl.rcParams['pdf.fonttype'] = 42
    mpl.rcParams['font.sans-serif'] = ['Helvetica', 'Helvetica Neue']


def set_axis_size(ax, w, h):
    """ w, h: width, height in inches """
    l = ax.figure.subplotpars.left
    r = ax.figure.subplotpars.right
    t = ax.figure.subplotpars.top
    b = ax.figure.subplotpars.bottom
    figw = float(w)/(r-l)
    figh = float(h)/(t-b)
    ax.figure.set_size_inches(figw, figh)


def format_axis_labels(ax, axis_info, despine=True, trim=False):
    if 'xlabel' in axis_info:
        ax.set_xlabel(axis_info['xlabel'])
    if 'ylabel' in axis_info:
        ax.set_ylabel(axis_info['ylabel'])
    if 'xmax' in axis_info:
        ax.set_xlim(axis_info.get('xstart', -0.5), axis_info['xmax'])
    if 'ymax' in axis_info:
        ax.set_ylim(axis_info.get('ystart', -0.5), axis_info['ymax'])
    if despine:
        sns.despine(offset=5, trim=trim, ax=ax)


def format_axis_fonts(ax, label_font=axis_label_font, tick_font=axis_tick_font, ytick_int=False, xtick_int=False, xprecision=1, yprecision=1):
    ax.set_xlabel(ax.get_xlabel(), fontdict=label_font)
    ax.set_ylabel(ax.get_ylabel(), fontdict=label_font)

    if ytick_int:
        yformat_str = '{:d}'
        ax.set_yticklabels([yformat_str.format(int(y)) for y in ax.get_yticks()],
                           fontdict=tick_font)
    else:
        yformat_str = '{:.{yprecision}f}'
        ax.set_yticklabels([yformat_str.format(y, yprecision=yprecision) for y in ax.get_yticks()],
                           fontdict=tick_font)

    if xtick_int:
        xformat_str = '{:d}'
        ax.set_xticklabels([xformat_str.format(int(x)) for x in ax.get_xticks()],
                           fontdict=tick_font)

    else:
        xformat_str = '{:.{xprecision}f}'
        ax.set_xticklabels([xformat_str.format(x, xprecision=xprecision) for x in ax.get_xticks()],
                           fontdict=tick_font)


def assign_stars(pvals, star_ths):
    """Assign significance stars based on pvalue thresholds.

    Parameters
    ----------
    pvals : np.array
        pvalues of data
    star_ths : 
        iith entry is ii+1 star max threshold

    Returns
    -------
    number_stars : np.array
        number of stars for datapoints in pvals
    """
    n_stars = np.zeros(len(pvals))
    for ii, star in enumerate(star_ths):
        n_stars[pvals < star] = ii+1
    return n_stars


def plot_stars(xs, ys, n_stars=None, pvals=None, star_ths=None, ax=None, xytext=(5, 0), fontsize=12, fontweight=100, color=None, horizontalalignment='left'):
    """ Plot significance stars at an offset from data specified by xs, ys with an offset of xytest.
    """
    if ax is None:
        ax = plt.gca()
    if n_stars is None:
        n_stars = assign_stars(p_vals, star_ths)
    for x, y, ns in zip(xs, ys, n_stars):
        if ns > 0:
            ax.annotate('*'*int(ns),
                        (x, y),
                        textcoords='offset points',
                        xytext=xytext,
                        fontsize=fontsize,
                        fontweight=fontweight,
                        color=color,
                        horizontalalignment=horizontalalignment)


def donut_plot(dist, ax=None, inner_radius=0.7, outer_radius=1, **kwargs):
    """Make a donut plot from a pie chart.

    Parameters
    ----------
    dist : array-like
        List of counts
    ax : matplotlib.axis, optional
        Axis to use, by default None
    inner_radius : float, optional
        Inner radius of the donut, by default 0.7
    outer_radius : int, optional
        Outer radius of the donut, by default 1
    """
    if ax is None:
        fig, ax = plt.subplots()
    ax.pie(dist, radius=outer_radius, **kwargs)
    circ = plt.Circle((0, 0), inner_radius, color='white')
    ax.add_artist(circ)
