"""
src/python/config.py
"""

import argparse
import configparser
import logging
import pathlib
import socket
import sys
import typing

log = logging.getLogger()


# -----------------------------------------------------------------------------

PROJECT_ROOT = pathlib.Path( __file__ ).parents[ 2 ]
PROJECT_NAME = PROJECT_ROOT.name
CONFIG_DIR = PROJECT_ROOT / 'etc' / 'config'


# -----------------------------------------------------------------------------

print( CONFIG_DIR / 'defaults.ini' )

parser = configparser.ConfigParser()
parser.read( CONFIG_DIR / 'defaults.ini' )
DEFAULTS = {
    'environment': 'development',
    'system': '',
    'dry_run': False,
    'logging_level': 'INFO',
    'logging_level_ext': 'INFO',
}


# -----------------------------------------------------------------------------


class Settings:
    """
    represents a .ini file found at <FILENAME_INI>
    <FILENAME_INI> is <CONFIG_DIR>/<SYSTEM>/<ENVIRONMENT>.ini
    <CONFIG_DIR> is <PROJECT_ROOT>/etc/config/ 
    """


    def __init__( self, args: argparse.Namespace ) -> None:
        """
        :param: args
        """

        self._args = args
        self._parser = configparser.ConfigParser()
        self._parser.read( self.config_ini_path.as_posix() )


    # ---------------------------------------------------------------------------------------------------

    @property
    def lock_file_path_name( self ):
        return f'/tmp/{PROJECT_NAME}-{self.system}-{self.environment}'


    # ---------------------------------------------------------------------------------------------------

    @property
    def dry_run( self ):
        return self._args.dry_run


    @property
    def max_depth( self ):
        return self._args.max_depth


    @property
    def system( self ):
        return self._args.system.lower()


    @property
    def environment( self ):
        return self._args.environment.lower()


    @property
    def config_ini_path( self ) -> pathlib.Path:
        return CONFIG_DIR / self.system / f'{self.environment.upper()}.ini'


    # ---------------------------------------------------------------------------------------------------

    @property
    def logging_level( self ) -> str:
        return self._args.logging_level or self._parser.get( 'logging', 'level', fallback='' )


    @property
    def logging_level_ext( self ) -> str:
        return self._args.logging_level_ext or self._parser.get( 'logging', 'level_ext', fallback='' )

