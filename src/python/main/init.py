"""
src/python/init.py
"""

import argparse
import logging
import time

log = logging.getLogger()


def init_logging( logging_level='INFO', logging_level_ext='ERROR' ) -> None:

    logging.basicConfig( datefmt='%Y-%m-%dT%H:%M:%S', format='{asctime}.{msecs:0<3.0f}  {levelname[0]}  {filename:>16}:{lineno:<3}  {funcName:<32}  {message}', style='{' )
    logging.Formatter.converter = time.gmtime
    logging.getLogger().setLevel( logging_level )

    logging.basicConfig(
        datefmt='%Y-%m-%dT%H:%M:%S',
        format='{asctime}.{msecs:0<3.0f}  {process:<6}  {levelname[0]}  {filename:>16}:{lineno:<3}  {funcName:<24}  {message}',
        level=logging.INFO,
        style='{'
    )
    logging.Formatter.converter = time.gmtime
    logging.getLogger().setLevel( logging_level )

    logging.getLogger( 'boto3' ).setLevel( logging_level_ext )
    logging.getLogger( 'botocore' ).setLevel( logging_level_ext )
    logging.getLogger( 'requests' ).setLevel( logging_level_ext )
    logging.getLogger( 's3transfer.futures' ).setLevel( logging_level_ext )
    logging.getLogger( 's3transfer.tasks' ).setLevel( logging_level_ext )
    logging.getLogger( 's3transfer.utils' ).setLevel( logging_level_ext )
    logging.getLogger( 'urllib3' ).setLevel( logging_level_ext )

