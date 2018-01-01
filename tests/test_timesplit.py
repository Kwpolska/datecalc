#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Date Calculator test suite
# Copyright © 2016-2018, Chris Warrick.
# See /LICENSE for licensing information.

"""Test TimeSplit."""

import pytest
from datecalc.utils import TimeSplit


def test_timesplit_init():
    """Test TimeSplit initialization."""
    ts = TimeSplit(-93784)
    assert ts.days == 1
    assert ts.hours == 2
    assert ts.minutes == 3
    assert ts.seconds == 4
    assert ts.is_negative
    ts = TimeSplit(59.9)
    assert ts.days == ts.hours == ts.minutes == 0
    assert ts.seconds == 59
    assert not ts.is_negative


def test_timesplit_str():
    """Test TimeSplit __str__ method."""
    cases = [
        (333, "00:05:33"),
        (3723, "01:02:03"),
        (93784, "1 day 02:03:04"),
        (1209600, "14 days 00:00:00"),
        (-93784, "-1 day 02:03:04"),
        (-1209600, "-14 days 00:00:00"),
        (-1, "-00:00:01"),
        (-3600, "-01:00:00"),
    ]

    for case_in, case_out in cases:
        assert str(TimeSplit(case_in)) == case_out


def test_timesplit_repr():
    """Test TimeSplit __repr__ method."""
    cases = [
        (333, "<TimeSplit 00:05:33>"),
        (3723, "<TimeSplit 01:02:03>"),
        (93784, "<TimeSplit 1d02:03:04>"),
        (1209600, "<TimeSplit 14d00:00:00>"),
        (-93784, "<TimeSplit -1d02:03:04>"),
        (-1209600, "<TimeSplit -14d00:00:00>"),
        (-1, "<TimeSplit -00:00:01>"),
        (-3600, "<TimeSplit -01:00:00>"),
    ]

    for case_in, case_out in cases:
        assert repr(TimeSplit(case_in)) == case_out


def test_timesplit_sanitize_values():
    """Test TimeSplit value sanitization."""
    ts = TimeSplit(60)
    ts.sanitize_values()
    assert ts.minutes == 1 and ts.seconds == 0

    ts.minutes = 0
    ts.seconds = 60
    ts.sanitize_values()
    assert ts.minutes == 1 and ts.seconds == 0
    ts.minutes = 61
    ts.seconds = 63
    ts.sanitize_values()
    assert ts.hours == 1 and ts.minutes == 2 and ts.seconds == 3
    ts.hours = 26
    ts.sanitize_values()
    assert ts.hours == 2 and ts.days == 1


def test_timesplit_to_seconds():
    """Test timesplit conversion to seconds."""
    cases = [1, -1, 60, 123, 3600, 3601, 86401, 93784]
    for case in cases:
        assert TimeSplit(case).to_seconds() == case


def test_timesplit_to_timedelta():
    """Test timesplit conversion to timedelta."""
    cases = [1, -1, 60, 123, 3600, 3601, 86401, 93784]
    for case in cases:
        assert TimeSplit(case).to_timedelta().total_seconds() == case


def test_timesplit_from_dhms():
    """Test TimeSplit creation from DHMS."""
    cases = [
        (0, 0, 5, 3, False),
        (0, 1, 2, 3, False),
        (1, 2, 3, 4, False),
        (1, 2, 3, 4, True),
    ]
    for d, h, m, s, n in cases:
        ts = TimeSplit.from_dhms(d, h, m, s, n)
        assert ts.days == d
        assert ts.hours == h
        assert ts.minutes == m
        assert ts.seconds == s
        assert ts.is_negative == n

    ts = TimeSplit.from_dhms(0, 0, 0, 60)
    assert ts.seconds == 60
    ts.sanitize_values()
    assert ts.minutes == 1 and ts.seconds == 0


def test_timesplit_from_timestring():
    """Test TimeSplit creation from time strings."""
    cases = [
        ("1d02:03:04", 1, 2, 3, 4, False),
        ("001d02:03:04", 1, 2, 3, 4, False),
        ("-1d02:03:04", 1, 2, 3, 4, True),
        ("m1d02:03:04", 1, 2, 3, 4, True),
        ("M1d02:03:04", 1, 2, 3, 4, True),
        ("10d200:03:04", 10, 200, 3, 4, False),
        ("1D02:03:04", 1, 2, 3, 4, False),
        ("1:02:03:04", 1, 2, 3, 4, False),
        ("01:02:03:04", 1, 2, 3, 4, False),
        ("+01:02:03:04", 1, 2, 3, 4, False),

        ("11 days 200:03:04", 11, 200, 3, 4, False),
        ("12 day 200:03:04", 12, 200, 3, 4, False),
        ("13 Days 200:03:04", 13, 200, 3, 4, False),
        ("14 Day 200:03:04", 14, 200, 3, 4, False),
        ("15DayS200:03:04", 15, 200, 3, 4, False),
        ("16DaYS 200:03:04", 16, 200, 3, 4, False),
        ("17 dAyS200:03:04", 17, 200, 3, 4, False),
        ("18DaY 200:03:04", 18, 200, 3, 4, False),
        ("19 dAy200:03:04", 19, 200, 3, 4, False),
        ("-20 days 200:03:04", 20, 200, 3, 4, True),

        ("01:02:03", 0, 1, 2, 3, False),
        ("-01:02:03", 0, 1, 2, 3, True),
        ("-1:2:3", 0, 1, 2, 3, True),
        ("001:002:003", 0, 1, 2, 3, False),
        ("100:200:300", 0, 100, 200, 300, False),

        ("1:2", 0, 0, 1, 2, False),
        ("1:02", 0, 0, 1, 2, False),
        ("M01:02", 0, 0, 1, 2, True),
        ("01:002", 0, 0, 1, 2, False),
        ("03:600", 0, 0, 3, 600, False),


        ("1", 0, 0, 0, 1, False),
        ("12", 0, 0, 0, 12, False),
        ("999", 0, 0, 0, 999, False),
        ("-78", 0, 0, 0, 78, True),
        ("m34", 0, 0, 0, 34, True),
        ("M56", 0, 0, 0, 56, True),


        ("5d", 5, 0, 0, 0, False),
        ("m5D", 5, 0, 0, 0, True),
    ]

    for timestring, d, h, m, s, n in cases:
        ts = TimeSplit.from_timestring(timestring)
        assert ts.days == d
        assert ts.hours == h
        assert ts.minutes == m
        assert ts.seconds == s
        assert ts.is_negative == n
    with pytest.raises(ValueError):
        TimeSplit.from_timestring("foobar")
