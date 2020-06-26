import os
import re


def dotdot_path():
    """Same as os.path.realpath('..')"""
    return os.path.realpath('..')


def define_dir(new_dir):
    """Make a directory if it does not yet exist"""
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
    return new_dir
