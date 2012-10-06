# -*- coding: utf-8 -*-
from __future__ import with_statement
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
    with raises(TypeError):
        list(Ranking([set([5]), set([4]), set([4]), set([3])],))
    def score(value):
        return list(value)[0]
    ranking = Ranking([set([5]), set([4]), set([4]), set([3])], score=score)
    assert ranking.ranks() == [0, 1, 1, 3]


@suite.test
def less_is_more():
    with raises(ValueError):
        list(Ranking([3, 4, 4, 5]))
    def compare(left, right):
        return -cmp(left, right)
    assert Ranking([3, 4, 4, 5], cmp=compare).ranks() == [0, 1, 1, 3]


@suite.test
def empty():
    assert list(Ranking([])) == []
    assert list(Ranking()) == []
