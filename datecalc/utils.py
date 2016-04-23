# -*- encoding: utf-8 -*-
# Date Calculator v0.1.0
# A simple date calculator.
# Copyright © 2016, Chris Warrick.
# See /LICENSE for licensing information.

"""
The logic for date calculations.

:Copyright: © 2016, Chris Warrick.
:License: BSD (see /LICENSE).
"""

import datetime
import dateutil.parser
import re

__all__ = ('TimeSplit', 'date_difference', 'dhms_to_seconds',
           'timestring_to_seconds', 'timestring_to_timedelta',
           'parse_date')

SEC_PER_DAY = 86400
SEC_PER_HOUR = 3600
SEC_PER_MINUTE = 60
_NEGATIVE_PART = r"^(?P<negative>[-+mM])?"
TIMESTRING_REGEX = (
    re.compile(_NEGATIVE_PART + r"(?P<days>\d+)[dD:]"
               r"(?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d+)$"),  # DHMS
    re.compile(_NEGATIVE_PART + r"(?P<days>\d+)[dD]"),  # D
    re.compile(_NEGATIVE_PART +
               r"(?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d+)$"),  # HMS
    re.compile(_NEGATIVE_PART +
               r"(?P<minutes>\d+):(?P<seconds>\d+)$"),  # MS
    re.compile(_NEGATIVE_PART + r"(?P<seconds>\d+)$"),  # S
)


class TimeSplit(object):
    """Time split into days, hours, minutes, seconds."""

    days = 0
    hours = 0
    minutes = 0
    seconds = 0

    def __init__(self, total_seconds):
        """Split time into days, hours, minutes, seconds.

        :param number total_seconds: Total seconds.
        """
        if total_seconds == 0:
            return
        self.is_negative = total_seconds < 0
        total_seconds = abs(int(total_seconds))  # ignore microseconds
        self.days, total_seconds = divmod(total_seconds, SEC_PER_DAY)
        self.hours, total_seconds = divmod(total_seconds, SEC_PER_HOUR)
        self.minutes, total_seconds = divmod(total_seconds, SEC_PER_MINUTE)
        self.seconds = total_seconds

    @classmethod
    def from_dhms(cls, days, hours, minutes, seconds, is_negative=False):
        """Convert days, hours, minutes, seconds into a TimeSplit object."""
        ts = cls(0)  # don’t re-calculate for now
        ts.days = days
        ts.hours = hours
        ts.minutes = minutes
        ts.seconds = seconds
        ts.is_negative = is_negative
        return ts

    @classmethod
    def from_timestring(cls, timestring):
        """Convert a time string to a TimeSplit object."""
        days, hours, minutes, seconds = 0, 0, 0, 0
        found = False
        for r in TIMESTRING_REGEX:
            m = r.match(timestring)
            if m:
                d = m.groupdict()
                negative = d.get('negative')
                days = d.get('days', 0)
                hours = d.get('hours', 0)
                minutes = d.get('minutes', 0)
                seconds = d.get('seconds', 0)
                found = True
                break

        days = int(days)
        hours = int(hours)
        minutes = int(minutes)
        seconds = int(seconds)

        if found:
            t = cls.from_dhms(days, hours, minutes, seconds)
            if negative in ('-', 'm', 'M'):
                t.is_negative = True
            return t
        else:
            raise ValueError("Time string does not match any template")

    def to_seconds(self):
        """Translate split time to total seconds."""
        total_seconds = dhms_to_seconds(
            self.days, self.hours, self.minutes, self.seconds)
        if self.is_negative:
            total_seconds = -total_seconds
        return total_seconds

    def sanitize_values(self):
        """Make sure all values are below their maximums."""
        if self.seconds >= 60:
            d, self.seconds = divmod(self.seconds, 60)
            self.minutes += d
        if self.minutes >= 60:
            d, self.minutes = divmod(self.minutes, 60)
            self.hours += d
        if self.hours >= 24:
            d, self.hours = divmod(self.hours, 24)
            self.days += d

    def __str__(self):
        """Stringify time."""
        if self.is_negative:
            s = '-'
        else:
            s = ''
        if self.days:
            s += '{0}d'.format(self.days)
        return s + '{0:02d}:{1:02d}:{2:02d}'.format(
            self.hours, self.minutes, self.seconds)

    def __repr__(self):
        """Programmer-friendly representation."""
        return "<TimeSplit {0!s}>".format(self)


def date_difference(start, end):
    """Calculate the difference between two datetime objects."""
    return TimeSplit((end - start).total_seconds())


def dhms_to_seconds(days, hours, minutes, seconds):
    """Convert days, hours, minutes, seconds to total seconds."""
    return ((days * SEC_PER_DAY) + (hours * SEC_PER_HOUR) +
            (minutes * SEC_PER_MINUTE) + seconds)


def timestring_to_seconds(timestring):
    """Convert a time string to total seconds."""
    return TimeSplit.from_timestring(timestring).to_seconds()


def timestring_to_timedelta(timestring):
    """Convert a time string to a timedelta object."""
    return datetime.timedelta(seconds=timestring_to_seconds(timestring))


def parse_date(date):
    """Parse date from string (also accepts 'now' and 'today')"""
    date = date.strip()
    datel = date.lower()
    if datel == 'now':  # pragma: no cover
        return datetime.datetime.now()
    elif datel == 'today':  # pragma: no cover
        return datetime.datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0)
    return dateutil.parser.parse(date)
