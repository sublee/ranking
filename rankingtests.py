# -*- coding: utf-8 -*-
from __future__ import with_statement
from attest import Tests, assert_hook, raises

from ranking import Ranking, COMPETITION, MODIFIED_COMPETITION, DENSE, \
                    ORDINAL, FRACTIONAL


suite = Tests()


@suite.test
def competition():
    assert Ranking([5, 4, 4, 3]).ranks() == [0, 1, 1, 3]


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
