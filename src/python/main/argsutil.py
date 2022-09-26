"""
src/python/main/argsutil.py
"""

import argparse
import typing

from config import DEFAULTS


def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser()

    action_choices=('cleanup', 'delete', 'dedupe', 'preen', 'unpreen', 'compress', 'evict-to-s3', 'prune')
    parser.add_argument( '--action', choices=action_choices, type=str.lower )

    site_choices=('ld4', 'nyc01', 'sg1', 'ty3', 'local')
    parser.add_argument( '--site', choices=site_choices, type=str.lower, default=None )

    environment_choices=('local', 'dev', 'uat', 'production')
    parser.add_argument( '--environment', choices=environment_choices, type=str.lower, default=DEFAULTS[ 'environment' ] )

    system_choices=('classic', 'enterprise')
    parser.add_argument( '--system', choices=system_choices, type=str.lower, default=DEFAULTS[ 'system' ] )

    parser.add_argument( '--dry-run', action='store_true', default=DEFAULTS[ 'dry_run' ] )
    parser.add_argument( '--no-dry-run', action='store_false', dest='dry_run', default=DEFAULTS[ 'dry_run' ] )

    logging_level_choices=('NOTSET', 'DEBUG', 'INFO', 'WARN', 'WARNING', 'ERROR', 'FATAL', 'CRITICAL')
    parser.add_argument( '--logging-level', choices=logging_level_choices, type=str.upper, default=DEFAULTS[ 'logging_level' ] )
    parser.add_argument( '--logging-level-ext', choices=logging_level_choices, type=str.upper, default=DEFAULTS[ 'logging_level_ext' ] )

    parser.add_argument( 'items', nargs=argparse.REMAINDER)

    args = parser.parse_args()

    return args

