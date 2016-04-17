# -*- encoding: utf-8 -*-
# Date Calculator v0.1.0
# A simple date calculator.
# Copyright © 2016, Chris Warrick.
# See /LICENSE for licensing information.

"""
Date Calculator command-line interface.

:Copyright: © 2016, Chris Warrick.
:License: BSD (see /LICENSE).
"""

import datecalc.utils
import argparse
import dateutil.parser
import sys

__all__ = ('main',)

arg_description = "A simple date calculator."
arg_epilog = """
DATE1 should be a date, DATE2 should be a date or a time string.
Date format: any, ISO 8601 preferred, watch out for spaces
Time string: DDdHH:MM:SS (all but seconds optional)
             Add 'm' for negative (or use -- and a minus sign)"""


def main():
    """The main routine of Date Calculator in CLI mode."""
    parser = argparse.ArgumentParser(
        description=arg_description, epilog=arg_epilog, add_help=True,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    operations = parser.add_mutually_exclusive_group(required=True)
    operations.add_argument(
        "-d", "--diff", action='store_true',
        help="Calculate difference between DATE1 and DATE2")
    operations.add_argument(
        "-a", "--add", action='store_true',
        help="Add/subtract DATE2 to/from DATE1")

    parser.add_argument("DATE1", help="Date to compare/operate on")
    parser.add_argument("DATE2", help="Date to compare/time to add")
    args = parser.parse_args()

    # Parse dates into appropriate things and act on them
    date1 = dateutil.parser.parse(args.DATE1)
    if args.diff:
        date2 = dateutil.parser.parse(args.DATE2)
        ts = datecalc.utils.date_difference(date1, date2)
        print(ts)
    elif args.add:
        date2 = datecalc.utils.timestring_to_timedelta(args.DATE2)
        new = date1 + date2
        print(new.isoformat())
    return 0

if __name__ == '__main__':
    sys.exit(main())
