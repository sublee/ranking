# -*- coding: utf-8 -*-
"""
    ranking
    ~~~~~~~

    :copyright: (c) 2012 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""


__copyright__ = 'Copyright 2012 by Heungsub Lee'
__license__ = 'BSD License'
__author__ = 'Heungsub Lee'
__email__ = 'h''@''subl.ee'
__version__ = '0.0.0'
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

    def __init__(self, iterable=[], strategy=COMPETITION, score=None, cmp=cmp):
        self.iterable = iterable
        self.strategy = strategy
        self.score = score
        self.cmp = cmp

    def __iter__(self):
        rank, draw = 0, []
        for left, right in zip(self.iterable[:-1], self.iterable[1:]):
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
        yield rank, right

    def iterranks(self):
        for rank, item in self:
            yield rank

    def ranks(self):
        return list(self.iterranks())
