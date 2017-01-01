#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Date Calculator test suite
# Copyright © 2016-2017, Chris Warrick.
# See /LICENSE for licensing information.

"""Test Date Calculator CLI."""

import datecalc.__main__  # NOQA
from datecalc.cli import main


def test_cli_d(capsys):
    """Test CLI (-d)."""
    main(["-d", "2016-01-01", "2016-01-02"])
    main(["-d", "2016-01-02", "2016-01-01"])
    main(["-d", "2016-01-01", "2016-01-03"])
    main(["-d", "2016-01-03", "2016-01-01"])
    out, err = capsys.readouterr()
    assert out == ('1 day 00:00:00\n-1 day 00:00:00\n'
                   '2 days 00:00:00\n-2 days 00:00:00\n')


def test_cli_a(capsys):
    """Test CLI (-a)."""
    main(["-a", "2016-01-02", "1d"])
    main(["-a", "2016-01-02", "m1d"])
    main(["-a", "2016-01-02", "M1d"])
    main(["-a", "2016-01-02", "--", "-1d"])
    out, err = capsys.readouterr()
    assert out == '\n'.join((
        '2016-01-03 00:00:00',
        '2016-01-01 00:00:00',
        '2016-01-01 00:00:00',
        '2016-01-01 00:00:00\n'))


def test_cli_vd(capsys):
    """Test CLI (-vd)."""
    main(["-vd", "2016-01-01", "2016-01-02"])
    main(["-vd", "2016-01-03", "2016-01-01"])
    out, err = capsys.readouterr()
    assert out == '\n'.join((
        '2016-01-01 00:00:00',
        '2016-01-02 00:00:00',
        '1 day 00:00:00',
        '2016-01-03 00:00:00',
        '2016-01-01 00:00:00',
        '-2 days 00:00:00\n'))


def test_cli_va(capsys):
    """Test CLI (-va)."""
    main(["-va", "2016-01-02", "2d"])
    main(["-va", "2016-01-02", "m1d"])
    out, err = capsys.readouterr()
    assert out == '\n'.join((
        '2016-01-02 00:00:00',
        '2 days 00:00:00',
        '2016-01-04 00:00:00',
        '2016-01-02 00:00:00',
        '-1 day 00:00:00',
        '2016-01-01 00:00:00\n'))
