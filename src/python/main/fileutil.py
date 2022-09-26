"""
src/python/main/fileutil.py
"""

import bz2
import gzip
import pathlib
import typing


def open_path( path: pathlib.Path ) -> typing.IO:
    """
    :param: pathname:
    :return: read-only file object
    """

    if path.suffix == '.gz':
        return gzip.GzipFile( path.as_posix() )

    elif path.suffix == '.bz2':
        return bz2.BZ2File( path.as_posix() )

    else:
        return open( path.as_posix(), 'rb' )
