#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Date Calculator test suite
# Copyright © 2016, Chris Warrick.
# See /LICENSE for licensing information.

"""Test Date Calculator CLI."""

import datecalc.__main__  # NOQA
from datecalc.cli import main


def test_cli(capsys):
    """Test CLI (-d)."""
    main(["-d", "2016-01-01", "2016-01-02"])
    main(["-d", "2016-01-02", "2016-01-01"])
    out, err = capsys.readouterr()
    assert out == '1d00:00:00\n-1d00:00:00\n'


def test_cli_a(capsys):
    """Test CLI (-a)."""
    main(["-a", "2016-01-02", "1d"])
    main(["-a", "2016-01-02", "m1d"])
    out, err = capsys.readouterr()
    assert out == '2016-01-03T00:00:00\n2016-01-01T00:00:00\n'
