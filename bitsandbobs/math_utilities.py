import numpy as np


def isbetween(d, start, end, start_inclusive=True, end_inclusive=False):
    """Return true where d is between start and end. By default inclusive of start and exclusive of end, but this is settable.

    Parameters
    ----------
    d : np.array
        data array
    start : int or float
        start value of window
    end : int or float
        end value of window
    start_inclusive : bool, optional
        Make window inclusive of the start value, by default True
    end_inclusive : bool, optional
        Make window inclusive of the end value, by default False

    Returns
    -------
    is_between : np.array
        Array with same size as d, True where values are between start and end.
    """
    if start_inclusive:
        l1 = d >= start
    else:
        l1 = d > start
    if end_inclusive:
        l2 = d <= end
    else:
        l2 = d < end
    return np.flatnonzero(np.logical_and(l1, l2))
