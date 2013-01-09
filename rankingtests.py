# -*- coding: utf-8 -*-
from __future__ import with_statement
from collections import defaultdict

from pytest import raises

from ranking import (Ranking, score_comparer, COMPETITION,
                     MODIFIED_COMPETITION, DENSE, ORDINAL, FRACTIONAL)


try:
    next
except NameError:
    # for Python 2.5
    next = lambda it: it.next()


def ranks(ranking):
    return list(ranking.ranks())


def test_competition():
    assert ranks(Ranking([5, 4, 4, 3], COMPETITION)) == [0, 1, 1, 3]


def test_modified_competition():
    assert ranks(Ranking([5, 4, 4, 3], MODIFIED_COMPETITION)) == [0, 2, 2, 3]


def test_dense():
    assert ranks(Ranking([5, 4, 4, 3], DENSE)) == [0, 1, 1, 2]


def test_ordinal():
    assert ranks(Ranking([5, 4, 4, 3], ORDINAL)) == [0, 1, 2, 3]


def test_fractional():
    assert ranks(Ranking([5, 4, 4, 3], FRACTIONAL)) == [0, 1.5, 1.5, 3]


def test_unsorted():
    with raises(ValueError):
        list(Ranking([5, 4, 4, 5]))


def test_strategies():
    strategies = [COMPETITION, MODIFIED_COMPETITION, DENSE, ORDINAL,
                  FRACTIONAL]
    for strategy in strategies:
        assert len(list(strategy(0, 2))) == 3


def test_capsuled_scores():
    class User(object):
        def __init__(self, score):
            self.score = score
        def __cmp__(self, other):
            raise NotImplemented
    users = [User(100), User(80), User(80), User(79)]
    with raises(TypeError):
        list(Ranking(users))
    key = lambda user: user.score
    ranking = Ranking(users, key=key)
    assert ranks(ranking) == [0, 1, 1, 3]
    assert isinstance(next(iter(ranking))[1], User)


def test_less_is_more():
    records = [1, 121, 121, 432, None, None]
    with raises(ValueError):
        list(Ranking(records))
    assert ranks(Ranking(records, reverse=True)) == [0, 1, 1, 3, None, None]


def test_empty():
    assert list(Ranking([])) == []
    with raises(TypeError):
        Ranking()


def test_start_from_not_zero():
    assert ranks(Ranking([5, 4, 4, 3], start=10)) == [10, 11, 11, 13]


def test_iterator_aware():
    scores = (x for x in range(100, 50, -10))
    assert ranks(Ranking(scores)) == [0, 1, 2, 3, 4]


def test_no_score_no_rank():
    assert ranks(Ranking([100, 50, 50, None, None])) == [0, 1, 1, None, None]
    assert ranks(Ranking([None])) == [None]
    assert ranks(Ranking([None, None])) == [None, None]
    assert ranks(Ranking([3, 1, 1, None])) == [0, 1, 1, None]


def test_custom_no_score():
    assert ranks(Ranking([100, 50, 50, -1, -1], no_score=-1)) == \
           [0, 1, 1, None, None]
    assert ranks(Ranking([-1], no_score=-1)) == [None]
    assert ranks(Ranking([-1, -1], no_score=-1)) == [None, None]
    assert ranks(Ranking([3, 1, 1, -1], no_score=-1)) == [0, 1, 1, None]
    assert ranks(Ranking([1, 1, 3, -1], reverse=True, no_score=-1)) == \
           [0, 0, 2, None]


def test_multiple_ties():
    assert ranks(Ranking([5, 5, 5, 3, 3, 3, 2, 2, 1, 1, 1, 1])) == \
           [0, 0, 0, 3, 3, 3, 6, 6, 8, 8, 8, 8]


def test_custom_strategy():
    def exclusive(start, length):
        return [None] * length + [start]
    assert ranks(Ranking([100, 80, 80, 70], exclusive)) == [0, None, None, 1]


def test_comparer_maker():
    cmp1 = score_comparer()
    cmp2 = score_comparer(key=lambda x: x[1])
    cmp3 = score_comparer(reverse=True)
    cmp4 = score_comparer(no_score=-1)
    try:
        [].sort(cmp=None)
    except TypeError:
        try:
            from functools import cmp_to_key
        except ImportError:
            # for Python 3.1
            def cmp_to_key(cmp):
                class K(object):
                    __slots__ = ['x']
                    __hash__ = None
                    def __init__(self, x): self.x = x
                    def __lt__(self, y): return cmp(self.x, y.x) < 0
                    def __gt__(self, y): return cmp(self.x, y.x) > 0
                    def __eq__(self, y): return cmp(self.x, y.x) == 0
                    def __le__(self, y): return cmp(self.x, y.x) <= 0
                    def __ge__(self, y): return cmp(self.x, y.x) >= 0
                    def __ne__(self, y): return cmp(self.x, y.x) != 0
                return K
        kw1 = {'key': cmp_to_key(cmp1)}
        kw2 = {'key': cmp_to_key(cmp2)}
        kw3 = {'key': cmp_to_key(cmp3)}
        kw4 = {'key': cmp_to_key(cmp4)}
    else:
        kw1 = {'cmp': cmp1}
        kw2 = {'cmp': cmp2}
        kw3 = {'cmp': cmp3}
        kw4 = {'cmp': cmp4}
    assert sorted([1, None, 5, 2], **kw1) == [5, 2, 1, None]
    assert sorted([[0, 1], [0, None], [0, 5], [0, 2]], **kw2) == \
           [[0, 5], [0, 2], [0, 1], [0, None]]
    assert sorted([1, None, 5, 2], **kw3) == [1, 2, 5, None]
    assert sorted([1, -1, 5, 2, -2], **kw4) == [5, 2, 1, -2, -1]
