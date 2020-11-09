import os
import re
import pandas as pd
from IPython.display import display


def _expand_path(pth):
    return os.path.abspath(os.path.expanduser(pth))


def dotdot_path():
    """Same as os.path.realpath('..')"""
    return _expand_path('..')


def dot_path():
    return _expand_path('.')


def define_dir(new_dir):
    print('Deprecated! Switch to "assert_dir"')
    return assert_dir(new_dir)


def assert_dir(new_dir):
    """Make a directory if it does not yet exist"""
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
    return _expand_path(new_dir)


def show_dataframe(df):
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        display(df)
