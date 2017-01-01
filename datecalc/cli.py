# -*- encoding: utf-8 -*-
# Date Calculator v0.2.1
# A simple date calculator.
# Copyright © 2016-2017, Chris Warrick.
# See /LICENSE for licensing information.

"""
Date Calculator command-line interface.

:Copyright: © 2016-2017, Chris Warrick.
:License: BSD (see /LICENSE).
"""

import datecalc
import datecalc.utils
import argparse
import sys

__all__ = ('main',)

arg_description = "A simple date calculator."
arg_epilog = """
DATE1 should be a date, DATE2 should be a date or a time string.
Date format: any, ISO 8601 preferred, watch out for spaces
             Use 'now' for current time, 'today' for today (midnight)
Time string: DDdHH:MM:SS (all but seconds optional)
             Add 'm' for negative (or use -- and a minus sign)"""


def main(src=None):
    """The main routine of Date Calculator in CLI mode."""
    parser = argparse.ArgumentParser(
        prog='datecalc', description=arg_description, epilog=arg_epilog,
        add_help=True, formatter_class=argparse.RawDescriptionHelpFormatter)

    operations = parser.add_mutually_exclusive_group(required=True)
    operations.add_argument(
        "-d", "--diff", action='store_true',
        help="Calculate difference between DATE1 and DATE2")
    operations.add_argument(
        "-a", "--add", action='store_true',
        help="Add/subtract DATE2 to/from DATE1")

    parser.add_argument(
        '--version', action='version',
        version='Date Calculator v{0}'.format(datecalc.__version__))
    parser.add_argument(
        "-v", "--verbose", action='store_true',
        help="Show dates before operating on them")
    parser.add_argument("DATE1", help="Date to compare/operate on")
    parser.add_argument("DATE2", help="Date to compare/time to add")
    if src is None:  # pragma: no cover
        args = parser.parse_args()
    else:
        args = parser.parse_args(src)

    # Parse dates into appropriate things and act on them

    date1 = datecalc.utils.parse_date(args.DATE1)
    if args.verbose:
        print(date1)
    if args.diff:
        date2 = datecalc.utils.parse_date(args.DATE2)
        if args.verbose:
            print(date2)
        ts = datecalc.utils.date_difference(date1, date2)
        print(ts)
    else:  # (args.add)
        date2 = datecalc.utils.TimeSplit.from_timestring(args.DATE2)
        if args.verbose:
            print(date2)
        new = date1 + date2.to_timedelta()
        print(new)

    return 0

if __name__ == '__main__':  # pragma: no cover
    sys.exit(main())
