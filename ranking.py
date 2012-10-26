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
__version__ = '0.2.3'
__license__ = 'BSD'
__author__ = 'Heungsub Lee'
__author_email__ = 'h''@''subl.ee'
__url__ = 'http://packages.python.org/ranking'
__all__ = ['Ranking', 'score_comparer', 'COMPETITION', 'MODIFIED_COMPETITION',
           'DENSE', 'ORDINAL', 'FRACTIONAL']


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


def score_comparer(key=None, reverse=False, no_score=None):
    """A helper function to generate a cmp function which is aware of score
    sorting rule.

        >>> my_cmp = score_comparer(no_score=-1) # -1 means "no score"
        >>> sorted([-3, -2, -1, 0, 1, 2], my_cmp)
        [2, 1, 0, -2, -3, -1]

    .. versionadded:: 0.2.3
    """
    def compare(left, right):
        left_score = left if key is None else key(left)
        if left_score == no_score:
            return 1
        right_score = right if key is None else key(right)
        if right_score == no_score:
            return -1
        compared = cmp(left_score, right_score)
        if not reverse:
            compared = -compared
        return compared
    return compare


class Ranking(object):
    """This class looks like `enumerate` but generates a `tuple` containing a
    rank and value instead.

    >>> scores = [100, 80, 80, 70, None]
    >>> list(ranking(scores))
    [(0, 100), (1, 80), (1, 80), (3, 70), (None, None)]

    :param sequence: sorted score sequence. `None` in the sequence means that
                     no score.
    :param strategy: a strategy for assigning rankings. Defaults to
                     :func:`COMPETITION`.
    :param start: a first rank. Defaults to 0.
    :param cmp: a comparation function. Defaults to :func:`cmp`.
    :param key: a function to get score from a value
    :param reverse: `sequence` is in ascending order if `True`, descending
                    otherwise. Defaults to `False`.
    :param no_score: a value for representing "no score". Defaults to `None`.
    """

    def __init__(self, sequence, strategy=COMPETITION, start=0, cmp=cmp,
                 key=None, reverse=False, no_score=None):
        self.sequence = sequence
        self.strategy = strategy
        self.start = start
        self.cmp = cmp
        self.key = key
        self.reverse = reverse
        self.no_score = no_score

    def __iter__(self):
        rank, drawn, tie_started, final = self.start, [], None, object()
        iterator = iter(self.sequence)
        right = iterator.next()
        right_score = right if self.key is None else self.key(right)
        for value in itertools.chain(iterator, [final]):
            left, right = right, value
            left_score = right_score
            if value is not final:
                right_score = right if self.key is None else self.key(right)
            if left_score == self.no_score:
                yield None, left
                continue
            elif right_score == self.no_score or value is final:
                compared = 1
            else:
                compared = self.cmp(left_score, right_score)
                if self.reverse:
                    compared = -compared
            if compared < 0: # left is less than right
                raise ValueError('%r should be behind of %r' % \
                                 (left_score, right_score))
            elif compared == 0: # same scores
                if tie_started is None:
                    tie_started = rank
                drawn.append(left)
                continue
            elif drawn:
                drawn.append(left)
                for rank in self.strategy(tie_started, len(drawn)):
                    try:
                        yield rank, drawn.pop(0)
                    except IndexError:
                        pass
                tie_started = None
                continue
            yield rank, left
            rank += 1

    def ranks(self):
        """Generates only ranks."""
        for rank, value in self:
            yield rank

    def rank(self, value):
        """Finds the rank of the value.

        :raises ValueError: the value isn't ranked in the ranking
        """
        for rank, other in self:
            if value == other:
                return rank
        raise ValueError('%r is not ranked' % value)
