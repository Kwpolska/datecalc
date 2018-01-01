#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Date Calculator test suite
# Copyright © 2016-2018, Chris Warrick.
# See /LICENSE for licensing information.

"""Test datecalc utilities."""

import datecalc.utils
import datetime


def test_date_difference():
    """Test date_difference."""
    dt1 = datetime.datetime(2016, 1, 1)
    dt2 = datecalc.utils.parse_date("2016-01-03 01:00:00")
    dd1 = datecalc.utils.date_difference(dt1, dt2)
    dd2 = datecalc.utils.date_difference(dt2, dt1)
    assert dd1.days == dd2.days == 2
    assert dd1.hours == dd2.hours == 1
    assert not dd1.is_negative
    assert dd2.is_negative


def test_dhms_to_seconds():
    """Test dhms_to_seconds()."""
    assert datecalc.utils.dhms_to_seconds(1, 2, 3, 4) == 93784
    assert datecalc.utils.dhms_to_seconds(0, 1, 0, 36) == 3636
    assert datecalc.utils.dhms_to_seconds(0, 0, 0, 1) == 1


def test_timestring_helpers():
    """Test timestring helper functions."""
    assert datecalc.utils.timestring_to_seconds("1:40") == 100
    assert datecalc.utils.timestring_to_timedelta("20").total_seconds() == 20
