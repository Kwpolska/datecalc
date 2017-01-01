===============
Date Calculator
===============
:Info: This is the README file for Date Calculator.
:Author: Chris Warrick <chris@chriswarrick.com>
:Copyright: © 2016-2017, Chris Warrick.
:Date: 2016-05-04
:Version: 0.2.1

.. index: README
.. image:: https://travis-ci.org/Kwpolska/datecalc.svg?branch=master
   :target: https://travis-ci.org/Kwpolska/datecalc

PURPOSE
-------

A simple date calculator that can calculate the difference between two dates or
add/subtract a given number of days, hours, minutes, seconds to a date.

INSTALLATION
------------

::

    pip install datecalc

CLI USAGE
---------

**Run:** ``datecalc``, ``datecalc-cli`` or ``python -m datecalc.cli``.

Calculating difference between dates:

::

    $ python -m datecalc.cli -d 2016-01-01T00:00:00 2016-01-02T02:03:04
    1 day 02:03:04
    $ python -m datecalc.cli -d 2016-01-02T02:03:04 2016-01-01T00:00:00
    -1 day 02:03:04
    $ python -m datecalc.cli -d 2016-01-01T00:00:00 2016-01-03T02:03:04
    2 days 02:03:04
    $ python -m datecalc.cli -d 2016-01-04T02:03:04 2016-01-01T00:00:00
    -3 days 02:03:04


Adding/subtracting:

::

    $ python -m datecalc.cli -a 2016-01-01T00:00:00 12:00:00
    2016-01-01T12:00:00
    $ python -m datecalc.cli -a 2016-01-01T00:00:00 m12:00:00
    2015-12-31T12:00:00
    $ python -m datecalc.cli -a -- 2016-01-01T00:00:00 -12:00:00
    2015-12-31T12:00:00
    $ python -m datecalc.cli -a 2016-01-01T00:00:00 4d12:00:00
    2016-01-05T12:00:00


GUI USAGE
---------

**Run:** ``datecalc-gui`` or ``python -m datecalc.gui``.
Date Calculator GUI requires PyQt5.

COPYRIGHT
---------
Copyright © 2016-2017, Chris Warrick.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

1. Redistributions of source code must retain the above copyright
   notice, this list of conditions, and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions, and the following disclaimer in the
   documentation and/or other materials provided with the distribution.

3. Neither the name of the author of this software nor the names of
   contributors to this software may be used to endorse or promote
   products derived from this software without specific prior written
   consent.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
