# -*- coding: utf-8 -*-
"""
    ranking
    ~~~~~~~

    :class:`Ranking` and various strategies for assigning rankings.

    :copyright: (c) 2012 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""


__copyright__ = 'Copyright 2012 by Heungsub Lee'
__license__ = 'BSD License'
__author__ = 'Heungsub Lee'
__email__ = 'h''@''subl.ee'
__version__ = '0.1.1'
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
    """:class:`Ranking` looks like :func:`enumerate` but generates a `tuple`
    containing a rank instead of an index and the values obtained from
    iterating over `sequence`:

    >>> scores = [10, 8, 7, 4]
    >>> list(Ranking(scores))
    [(0, 10), (1, 8), (2, 7), (3, 4)]

    In most cases, rank is equivalent to index. But which values would share
    same score. Then it follows a way that the strategy for assigning ranking
    describes. A strategy is a function that parameterized by `start`, `length`
    and assigns ranks to the tie scores and the next:

    >>> scores = [10, 8, 8, 6]
    >>> list(Ranking(scores)) # strategy defaults to COMPETITION
    [(0, 10), (1, 8), (1, 8), (3, 6)]
    >>> list(Ranking(scores, DENSE))
    [(0, 10), (1, 8), (1, 8), (2, 6)]
    >>> list(Ranking(scores, FRACTIONAL))
    [(0, 10), (1.5, 8), (1.5, 8), (3, 6)]
    >>> list(FRACTIONAL(1, 2))
    [1.5, 1.5, 3]

    :param sequence: sorted score sequence
    :param strategy: a strategy for assigning rankings. Defaults to
                     :func:`COMPETITION`.
    :param start: a first rank. Defaults to 0.
    :param score: a function to get score from a value
    :param cmp: a comparation function. Defaults to :func:`cmp`.
    """

    def __init__(self, sequence=None, strategy=COMPETITION, start=0, key=None,
                 cmp=cmp):
        if sequence is None:
            self.sequence = []
        else:
            self.sequence = sequence
        self.strategy = strategy
        self.start = start
        self.key = key
        self.cmp = cmp

    def __iter__(self):
        rank, draw = self.start, []
        for left, right in zip(self.sequence[:-1], self.sequence[1:]):
            if self.key is not None:
                left = self.key(left)
                right = self.key(right)
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
