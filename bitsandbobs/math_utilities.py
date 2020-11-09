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


def within_bbox(xyz, bbox):
    """Returns true when xyz in a bounding box

    Parameters
    ----------
    xyz : array
        Nx3 numpy array of points
    bbox : array
        2x3 array of upper, lower bounds of bounding box

    Returns
    -------
    within_bbox : array
        N-length boolean array, True for points inside bbox
    """
    within_x = np.logical_and(xyz[:, 0] > bbox[0, 0], xyz[:, 0] <= bbox[1, 0])
    within_y = np.logical_and(xyz[:, 1] > bbox[0, 1], xyz[:, 1] <= bbox[1, 1])
    within_z = np.logical_and(xyz[:, 2] > bbox[0, 2], xyz[:, 2] <= bbox[1, 2])
    return within_x & within_y & within_z
