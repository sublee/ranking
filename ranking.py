# -*- coding: utf-8 -*-
"""
    ranking
    ~~~~~~~

    :class:`Ranking` iterator and various strategies for assigning rankings.

    :copyright: (c) 2012 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""


__copyright__ = 'Copyright 2012 by Heungsub Lee'
__license__ = 'BSD License'
__author__ = 'Heungsub Lee'
__email__ = 'h''@''subl.ee'
__version__ = '0.1'
__all__ = ['Ranking', 'COMPETITION', 'MODIFIED_COMPETITION', 'DENSE',
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
    for x in xrange(length + 1):
        yield start + x


def FRACTIONAL(start, length):
    """Fractional ranking ("1 2.5 2.5 4" ranking)"""
    avg = (2 * start + length - 1) / float(length)
    for x in xrange(length):
        yield avg
    yield start + length


class Ranking(object):
    """:class:`Ranking` assigns rank to each value.

    :param values: sorted score sequence
    :param strategy: a strategy for assigning rankings. Defaults to
                     :func:`COMPETITION`.
    :param score: a function to get score from a value
    :param cmp: comparation function. Defaults to :func:`cmp`.
    """

    def __init__(self, values=[], strategy=COMPETITION, score=None, cmp=cmp):
        self.values = values
        self.strategy = strategy
        self.score = score
        self.cmp = cmp

    def __iter__(self):
        rank, draw = 0, []
        for left, right in zip(self.values[:-1], self.values[1:]):
            if self.score is not None:
                left = self.score(left)
                right = self.score(right)
            compared = self.cmp(left, right)
            if compared < 0: # left is less than right
                raise ValueError('Not sorted by score')
            elif compared == 0: # same scores
                draw.append((rank, left))
                continue
            elif draw: # left is more than right but there're saved draw scores
                draw.append((rank, left))
                for adopted_rank in self.strategy(draw[0][0], len(draw)):
                    try:
                        yield adopted_rank, draw.pop(0)[1]
                    except IndexError:
                        rank = adopted_rank
                continue
            yield rank, left
            rank += 1
        try:
            yield rank, right
        except UnboundLocalError:
            pass

    def iterranks(self):
        for rank, value in self:
            yield rank

    def ranks(self):
        return list(self.iterranks())

    def itervalues(self):
        for rank, value in self:
            yield value

    def values(self):
        return list(self.itervalues())
