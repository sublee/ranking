# -*- coding: utf-8 -*-
"""
    ranking
    ~~~~~~~

    :class:`Ranking` and various strategies for assigning rankings.

    :copyright: (c) 2012 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
import itertools


__copyright__ = 'Copyright 2012 by Heungsub Lee'
__version__ = '0.2'
__license__ = 'BSD'
__author__ = 'Heungsub Lee'
__author_email__ = 'h''@''subl.ee'
__url__ = 'http://packages.python.org/ranking'
__all__ = ['ranking', 'COMPETITION', 'MODIFIED_COMPETITION', 'DENSE',
           'ORDINAL', 'FRACTIONAL']


def COMPETITION(start, length):
    """Standard competition ranking ("1224" ranking)"""
    for x in xrange(length):
        yield start
    yield start + length


def MODIFIED_COMPETITION(start, length):
    """Modified competition ranking ("1334" ranking)"""
    for x in xrange(length):
        yield start + length - 1
    yield start + length


def DENSE(start, length):
    """Dense ranking ("1223" ranking)"""
    for x in xrange(length):
        yield start
    yield start + 1


def ORDINAL(start, length):
    """Ordinal ranking ("1234" ranking)"""
    return xrange(start, start + length + 1)


def FRACTIONAL(start, length):
    """Fractional ranking ("1 2.5 2.5 4" ranking)"""
    avg = (2 * start + length - 1) / float(length)
    for x in xrange(length):
        yield avg
    yield start + length


def ranking(sequence, strategy=COMPETITION, start=0, cmp=cmp, key=None):
    """:func:`ranking` looks like :func:`enumerate` but generates a `tuple`
    containing a rank instead of an index.

    >>> scores = [100, 80, 80, 70, None]
    >>> list(enumerate(scores))
    [(0, 100), (1, 80), (2, 80), (3, 70), (4, None)]
    >>> list(ranking(scores))
    [(0, 100), (1, 80), (1, 80), (3, 70), (None, None)]

    :param sequence: sorted score sequence
    :param strategy: a strategy for assigning rankings. Defaults to
                     :func:`COMPETITION`.
    :param start: a first rank. Defaults to 0.
    :param cmp: a comparation function. Defaults to :func:`cmp`.
    :param key: a function to get score from a value
    """
    rank, drawn, tie_started, final = start, [], None, object()
    iterator = iter(sequence)
    right = iterator.next()
    right_score = right if key is None else key(right)
    for value in itertools.chain(iterator, [final]):
        left, right = right, value
        left_score = right_score
        if value is not final:
            right_score = right if key is None else key(right)
        if left_score is None:
            yield None, left
            continue
        elif value is final:
            compared = 1
        else:
            compared = cmp(left_score, right_score)
        if compared < 0: # left is less than right
            raise ValueError('Not sorted by score')
        elif compared == 0: # same scores
            if tie_started is None:
                tie_started = rank
            drawn.append(left)
            continue
        elif drawn:
            drawn.append(left)
            for rank in strategy(tie_started, len(drawn)):
                try:
                    yield rank, drawn.pop(0)
                except IndexError:
                    pass
            tie_started = None
            continue
        yield rank, left
        rank += 1
