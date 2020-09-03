from multiwrapper import multiprocessing_utils as mu
import cloudvolume
import numpy as np
import datetime


def cv_download_points(points, cv, res=np.array([4, 4, 40]), mip=0, root_ids=True, n_threads=10, timestamp=None):
    """Download a collection of individual root ids (or supervoxel ids).

    Parameters
    ----------
    points : array
        Nx3 numpy array of locations in neuroglancer at the resolution specified.
    cv : cloudvolume.CloudVolume
        CloudVolume instance
    res : array, optional
        3 element array specifing the resolution of the points, by default np.array([4, 4, 40])
    mip : int, optional
        Mip to query, by default 0
    root_ids : bool, optional
        If True, returns root ids. If False, returns supervoxels. By default True.
    n_threads : int, optional
        Number of threads to use for the download, by default 10
    timestamp : float, optional
        UTC stamp for proofreading lookup. 

    Returns
    -------
    root_ids : array
        Root ids / supervoxel ids at each of the points
    """
    if timestamp is None:
        timestamp = datetime.datetime.now().timestamp()

    points_remap = np.array(points) * res / np.array(cv.mip_resolution(0))
    args = [[p, cv] for p in points_remap]

    def _dl_point(args):
        p, cv = args
        bbox = cloudvolume.Bbox(p.astype(int), p.astype(int)+1)
        return int(np.array(cv.download(bbox, agglomerate=root_ids, timestamp=timestamp)).squeeze())

    return mu.multithread_func(_dl_point, args, n_threads=n_threads)
