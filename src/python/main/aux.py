"""
src/python/main/aux.py
"""

import argparse
import fcntl
import hashlib
import logging
import pathlib
import sys

import config
import fileutil

log = logging.getLogger()


def get_lock( lock_file_path_name: str ):
    """
    get_lock

    :param: lock_file_path_name:
    :return:
    """

    try:
        flock_fp = open( lock_file_path_name, 'w' )
        fcntl.flock( flock_fp, fcntl.LOCK_EX | fcntl.LOCK_NB )
        log.debug( f'acquired lock [{flock_fp}]' )
    except IOError as ioe:
        log.error( f'error: could not get lock on [{lock_file_path_name}]' )
        sys.exit( 111 )

    return flock_fp


def compare_path_contents( path_one: pathlib.Path, path_two: pathlib.Path ) -> bool:
    """
    compare_path_contents

    :param: path_one:
    :param: path_two:
    :return:
    """


    def hexdigest_from_path( p: pathlib.Path ):
        return hashlib.md5( fileutil.open_path( p ).read(), usedforsecurity=False ).hexdigest()


    if not path_one.exists():
        return False
    hexdigest_one = hexdigest_from_path( path_one )

    if not path_two.exists():
        return False
    hexdigest_two = hexdigest_from_path( path_two )

    return hexdigest_one == hexdigest_two


def announce( s: config.Settings, args: argparse.Namespace ) -> None:
    """
    announce

    :param args: command-line args from argparse
    :param s: settings object
    :return:
    """

    log.info( f'' )
    log.info( f'dry_run          [{args.dry_run}]' )
    log.info( f'action           [{args.action}]' )
    log.info( f'system           [{s.system}]' )
    log.info( f'environment      [{args.environment}]' )
    log.info( f'config_ini_path  [{s.config_ini_path}]' )
    log.info( f'' )
