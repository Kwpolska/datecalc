# -*- encoding: utf-8 -*-
# Date Calculator v0.2.1
# A simple date calculator.
# Copyright © 2016-2021, Chris Warrick.
# See /LICENSE for licensing information.

"""
Date Calculator main entry-point (defaults to CLI).

:Copyright: © 2016-2021, Chris Warrick.
:License: BSD (see /LICENSE).
"""

import datecalc.cli
import sys

__all__ = ()


if __name__ == '__main__':  # pragma: no cover
    sys.exit(datecalc.cli.main())
