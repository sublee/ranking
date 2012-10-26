# -*- coding: utf-8 -*-
from __future__ import with_statement
from collections import defaultdict

from attest import Tests, assert_hook, raises

from ranking import Ranking, COMPETITION, MODIFIED_COMPETITION, DENSE, \
                    ORDINAL, FRACTIONAL


suite = Tests()


def ranks(ranking):
    return list(ranking.ranks())


@suite.test
def competition():
    assert ranks(Ranking([5, 4, 4, 3], COMPETITION)) == [0, 1, 1, 3]


@suite.test
def modified_competition():
    assert ranks(Ranking([5, 4, 4, 3], MODIFIED_COMPETITION)) == [0, 2, 2, 3]


@suite.test
def dense():
    assert ranks(Ranking([5, 4, 4, 3], DENSE)) == [0, 1, 1, 2]


@suite.test
def ordinal():
    assert ranks(Ranking([5, 4, 4, 3], ORDINAL)) == [0, 1, 2, 3]


@suite.test
def fractional():
    assert ranks(Ranking([5, 4, 4, 3], FRACTIONAL)) == [0, 1.5, 1.5, 3]


@suite.test
def unsorted():
    with raises(ValueError):
        list(Ranking([5, 4, 4, 5]))


@suite.test
def strategies():
    strategies = [COMPETITION, MODIFIED_COMPETITION, DENSE, ORDINAL,
                  FRACTIONAL]
    for strategy in strategies:
        assert len(list(strategy(0, 2))) == 3


@suite.test
def capsuled_scores():
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
    assert isinstance(iter(ranking).next()[1], User)


@suite.test
def less_is_more():
    records = [1, 121, 121, 432, None, None]
    with raises(ValueError):
        list(Ranking(records))
    assert ranks(Ranking(records, reverse=True)) == [0, 1, 1, 3, None, None]


@suite.test
def empty():
    assert list(Ranking([])) == []
    with raises(TypeError):
        Ranking()


@suite.test
def start_from_not_zero():
    assert ranks(Ranking([5, 4, 4, 3], start=10)) == [10, 11, 11, 13]


@suite.test
def iterator_aware():
    scores = xrange(100, 50, -10)
    assert ranks(Ranking(scores)) == [0, 1, 2, 3, 4]


@suite.test
def no_score_no_rank():
    assert ranks(Ranking([100, 50, 50, None, None])) == [0, 1, 1, None, None]
    assert ranks(Ranking([None])) == [None]
    assert ranks(Ranking([None, None])) == [None, None]
    assert ranks(Ranking([3, 1, 1, None])) == [0, 1, 1, None]


@suite.test
def multiple_ties():
    assert ranks(Ranking([5, 5, 5, 3, 3, 3, 2, 2, 1, 1, 1, 1])) == \
           [0, 0, 0, 3, 3, 3, 6, 6, 8, 8, 8, 8]


@suite.test
def custom_strategy():
    def exclusive(start, length):
        return [None] * length + [start]
    assert ranks(Ranking([100, 80, 80, 70], exclusive)) == [0, None, None, 1]
