# -*- coding: utf-8 -*-
from __future__ import with_statement
from collections import defaultdict

from attest import Tests, assert_hook, raises

from ranking import Ranking, COMPETITION, MODIFIED_COMPETITION, DENSE, \
                    ORDINAL, FRACTIONAL


suite = Tests()


@suite.test
def competition():
    assert Ranking([5, 4, 4, 3], COMPETITION).ranks() == [0, 1, 1, 3]


@suite.test
def modified_competition():
    assert Ranking([5, 4, 4, 3], MODIFIED_COMPETITION).ranks() == [0, 2, 2, 3]


@suite.test
def dense():
    assert Ranking([5, 4, 4, 3], DENSE).ranks() == [0, 1, 1, 2]


@suite.test
def ordinal():
    assert Ranking([5, 4, 4, 3], ORDINAL).ranks() == [0, 1, 2, 3]


@suite.test
def fractional():
    assert Ranking([5, 4, 4, 3], FRACTIONAL).ranks() == [0, 1.5, 1.5, 3]


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
    assert Ranking(users, key=lambda user: user.score).ranks() == [0, 1, 1, 3]


@suite.test
def less_is_more():
    records = [1, 121, 121, 432]
    with raises(ValueError):
        list(Ranking(records))
    def reverse_cmp(left, right):
        return -cmp(left, right)
    assert Ranking(records, cmp=reverse_cmp).ranks() == [0, 1, 1, 3]


@suite.test
def empty():
    assert list(Ranking([])) == []
    assert list(Ranking()) == []


@suite.test
def start_from_not_zero():
    assert Ranking([5, 4, 4, 3], start=10).ranks() == [10, 11, 11, 13]


@suite.test
def score_generator():
    scores = xrange(100, 50, -10)
    assert Ranking(scores).ranks() == [0, 1, 2, 3, 4]
