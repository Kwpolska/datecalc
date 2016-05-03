#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import io
from setuptools import setup, find_packages


setup(name='datecalc',
      version='0.1.1',
      description='A simple date calculator.',
      keywords='datecalc,date,time',
      author='Chris Warrick',
      author_email='chris@chriswarrick.com',
      url='https://github.com/Kwpolska/datecalc',
      license='3-clause BSD',
      long_description=io.open(
          './docs/README.rst', 'r', encoding='utf-8').read(),
      platforms='any',
      zip_safe=False,
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Development Status :: 3 - Alpha',
                   'Environment :: Console',
                   'License :: OSI Approved :: BSD License',
                   'Topic :: Utilities',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5'],
      packages=find_packages(),
      include_package_data=True,
      install_requires=['python-dateutil'],
      extras_require={'gui': ['PyQt5']},
      data_files=[('share/applications', ['freedesktop/datecalc.desktop'])],
      entry_points={
          'console_scripts': [
              'datecalc = datecalc.cli:main',
              'datecalc-cli = datecalc.cli:main',
          ],
          'gui_scripts': [
              'datecalc-gui = datecalc.gui:main',
          ]
      },
      )
