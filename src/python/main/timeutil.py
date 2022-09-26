"""
src/python/timeutil.py
"""

import datetime
import logging
import re

log = logging.getLogger()


class SimpleContextTimer:

    def __enter__( self ):
        self._start = datetime.datetime.utcnow()
        return self


    def __exit__( self, *args ):
        self._end = datetime.datetime.utcnow()


    @property
    def duration( self ) -> datetime.timedelta:
        return self._end - self._start


def text_from_timedelta( td: datetime.timedelta ) -> str:
    """
    :param: td:
    :return:
    """

    remainder = td.total_seconds()
    weeks, remainder = divmod( remainder, 7 * 24 * 60 * 60 )
    days, remainder = divmod( remainder, 24 * 60 * 60 )
    hours, remainder = divmod( remainder, 60 * 60 )
    minutes, seconds = divmod( remainder, 60 )

    return f'{weeks:.0f}w, {days:.0f}d, {hours:.0f}h, {minutes:.0f}m, {seconds:.0f}s'


def timedelta_from_text( text: str ) -> datetime.timedelta:
    """
    :param: text:
    :return:
    """

    if not text:
        raise ValueError( 'non-empty value for "text" required' )

    unit_name_list = ('weeks', 'days', 'hours', 'minutes', 'seconds')
    expression = ''.join( [ f'(?:(?P<{unit}>\\d+)(\\s*{unit}?[, ]*))?' for unit in unit_name_list ] )
    match = re.search( expression, text, re.IGNORECASE )
    d = { unit: int( match.groupdict().get( unit ) or 0 ) for unit in unit_name_list }
    td = datetime.timedelta( **d )

    if td.total_seconds() == 0:
        raise ValueError( f'[{text}] does not match required format "[N week[s], ][N day[s], ][N hour[s], ][N minute[s], ][N second[s]]"' )

    return td
