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


def lookup_svids(svids, client, timestamp=None, batch_size=500, n_threads=16):
    """Look up a list of supervoxel ids with multiprocessing

    Parameters
    ----------
    svids : array
        N-length array of supervoxel ids (can include 0s)
    client : annotationframeworkclient.FrameworkClient
        Client to access chunkedgraph services
    timestamp : datetime.datetime or None, optional
        Timestamp for lookup, by default None (defaults to now)
    batch_size : int, optional
        Estimated batch size per root lookup, by default 500
    n_threads : int, optional
        Number of threads to use, by default 16

    Returns
    -------
    root_ids : array
        N-length array of root ids with 0s where svid was 0
    """
    n_groups = len(svids) // batch_size
    sv_groups = np.array_split(svids, n_groups)

    if timestamp is None:
        timestamp = datetime.datetime.now()

    args = []
    for svg in sv_groups:
        args.append((svg, client, timestamp))
    rids = mu.multithread_func(_mu_lookup_svids, args, n_threads=n_threads)
    return np.concatenate(rids)


def _mu_lookup_svids(args):
    svids, client, timestamp = args
    return _lookup_svids(svids, client, timestamp)


def _lookup_svids(svids, client, timestamp=None):
    svids_full = np.zeros(len(svids), dtype=np.int64)
    nonzero_svids = np.flatnonzero(svids != 0)
    svids_full[nonzero_svids] = client.chunkedgraph.get_roots(svids[nonzero_svids],
                                                              timestamp=timestamp)
    return svids_full
