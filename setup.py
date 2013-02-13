# -*- coding: utf-8 -*-
"""
Ranking
~~~~~~~

This library provides ``Ranking`` iterator to assign rank to each values and
various `strategies for assigning rankings`_.

>>> sorted_scores = [100, 90, 90, 80, 70]
>>> for rank, score in Ranking(sorted_scores):
...     print '%d. %d' % (rank + 1, score)
1. 100
2. 90
2. 90
4. 80
5. 70
>>> for rank, score in Ranking(sorted_scores, DENSE):
...     print '%d. %d' % (rank + 1, score)
1. 100
2. 90
2. 90
3. 80
4. 70

Links
`````

* `GitHub repository <http://github.com/sublee/ranking>`_
* `development version
  <http://github.com/sublee/ranking/zipball/master#egg=ranking-dev>`_

.. _strategies for assigning rankings: 
   http://en.wikipedia.org/wiki/Ranking#Strategies_for_assigning_rankings

"""
from __future__ import with_statement
import re
from setuptools import setup
from setuptools.command.test import test
import sys


# detect the current version
with open('ranking.py') as f:
    version = re.search(r'__version__\s*=\s*\'(.+?)\'', f.read()).group(1)
assert version


# use pytest instead
def run_tests(self):
    pyc = re.compile(r'\.pyc|\$py\.class')
    test_file = pyc.sub('.py', __import__(self.test_suite).__file__)
    raise SystemExit(__import__('pytest').main([test_file]))
test.run_tests = run_tests


setup(
    name='ranking',
    version=version,
    license='BSD',
    author='Heungsub Lee',
    author_email=re.sub('((sub).)(.*)', r'\2@\1.\3', 'sublee'),
    url='http://pythonhosted.org/ranking',
    description='Ranking collection',
    long_description=__doc__,
    platforms='any',
    py_modules=['ranking'],
    classifiers=['Development Status :: 1 - Planning',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.5',
                 'Programming Language :: Python :: 2.6',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.1',
                 'Programming Language :: Python :: 3.2',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: Implementation :: CPython',
                 'Programming Language :: Python :: Implementation :: Jython',
                 'Programming Language :: Python :: Implementation :: PyPy',
                 'Topic :: Games/Entertainment'],
    test_suite='rankingtests',
    tests_require=['pytest'],
    use_2to3=(sys.version_info[0] >= 3),
)
