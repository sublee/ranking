# -*- coding: utf-8 -*-
from setuptools import setup


setup(
    name='ranking',
    version='0.0.0',
    license='BSD',
    author='Heungsub Lee',
    author_email='h@subl.ee',
    description='Library for ranking collection',
    #long_description=__doc__,
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
    #test_suite='rankingtests.suite',
    #test_loader='attest:auto_reporter.test_loader',
    #tests_require=['Attest'],
)
