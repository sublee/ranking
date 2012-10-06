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
from setuptools import setup


setup(
    name='ranking',
    version='0.1',
    license='BSD',
    author='Heungsub Lee',
    author_email='h@subl.ee',
    description='Ranking collection',
    long_description=__doc__,
    platforms='any',
    py_modules=['ranking'],
    classifiers=['Development Status :: 1 - Planning',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2.5',
                 'Programming Language :: Python :: 2.6',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: Implementation :: CPython',
                 'Programming Language :: Python :: Implementation :: PyPy',
                 'Topic :: Games/Entertainment'],
    test_suite='rankingtests.suite',
    test_loader='attest:auto_reporter.test_loader',
    tests_require=['Attest'],
)
