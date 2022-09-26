"""
src/python/main.py
"""

import argparse
import logging
import sys

import argsutil
import aux
import cleanup
import compress
import config
import dedupe
import delete
import evict_to_s3
import init
import preen
import prune
import timeutil

log = logging.getLogger()


def check_settings( settings: config.Settings, args: argparse.Namespace ) -> None:
    """
    check_settings

    :return:
    """

    forbidden_combinations = {
        ('production', 'delete'): 'production data is never deleted',
        ('uat', 'evict-to-s3'): 'UAT data never goes to AWS S3'
    }

    reason = forbidden_combinations.get( (settings.environment, args.action) )
    if reason:
        log.error( f'fatal: forbidden environment / action combination: [{settings.environment}] / [{args.action}]: {reason}' )
        sys.exit( 111 )

    if settings.environment == 'production':
        if timeutil.timedelta_from_text( settings.age_evict_to_s3 ) < timeutil.timedelta_from_text( settings.age_compress ):
            log.error( f'fatal: age_evict_to_s3 [{settings.age_evict_to_s3}] is less than age_compress [{settings.age_compress}]' )
            sys.exit( 111 )

    if timeutil.timedelta_from_text( settings.age_compress ) < timeutil.timedelta_from_text( settings.age_preen ):
        log.error( f'fatal: age_compress [{settings.age_compress}] is less than age_preen [{settings.age_preen}]' )
        sys.exit( 111 )


def dispatch( s: config.Settings, a: argparse.Namespace ) -> None:
    """
    switch based on the value of args.action

    :param: args
    :return:
    """

    lock_fp = aux.get_lock( s.lock_file_path_name )

    if a.action == 'cleanup':
        cleanup.cleanup_tree( s )

    if a.action == 'dedupe':
        dedupe.dedupe_tree( s )

    if a.action == 'preen':
        preen.preen_tree( s )

    if a.action == 'unpreen':
        preen.unpreen_tree( s )

    if a.action == 'compress':
        compress.compress_tree( s )

    if a.action == 'evict-to-s3':
        evict_to_s3.evict_from_tree( s )

    if a.action == 'delete':
        delete.delete_files_from_tree( s )

    if a.action == 'prune':
        prune.prune_tree( s )


def main() -> None:
    """
    main

    :return:
    """

    init.init_logging_config()
    args = argsutil.parse_args()
    init.init_logging_levels( args )
    settings = config.Settings( args )
    aux.announce( settings, args )
    check_settings( settings, args )

    with timeutil.SimpleContextTimer() as timer:
        dispatch( settings, args )
    log.info( f'duration [{timeutil.text_from_timedelta( timer.duration )}]' )


if __name__ == '__main__':
    try:
        sys.exit( main() )
    except KeyboardInterrupt:
        sys.exit( 111 )
