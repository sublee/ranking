Ranking
=======

strategies to assign ranks

.. currentmodule:: ranking

Introduction
~~~~~~~~~~~~

In most cases, `enumerate` a Python standard function is a best tool to make a
ranking. But how about tie scores? You may end up with giving different rank
for tie scores. And I'm quite sure that will make you and your users
dissatisfied. Solution? You are on the right page.

::

   >>> list(enumerate([100, 80, 80, 70]))
   [(0, 100), (1, 80), (2, 80), (3, 70)]

This module implements :class:`Ranking` that looks like `enumerate` but
generates ranks instead of indexes and various strategy to assign ranks to tie
scores.

::

   >>> list(Ranking([100, 80, 80, 70])) # same scores have same ranks
   [(0, 100), (1, 80), (1, 80), (3, 70)]

API
~~~

.. autoclass:: Ranking
   :members:

Strategies to assign ranks
~~~~~~~~~~~~~~~~~~~~~~~~~~

:class:`Ranking` follows the strategy function when it assigns ranks to tie
scores. Also this module provides `most common 5 strategies <http://en.
wikipedia.org/wiki/Ranking#Strategies_for_assigning_rankings>`_:

.. autofunction:: COMPETITION
.. autofunction:: MODIFIED_COMPETITION
.. autofunction:: DENSE
.. autofunction:: ORDINAL
.. autofunction:: FRACTIONAL

You can also implement your own strategy function. A strategy function has
parameters `start`, a rank of the first tie score; `length`, a length of tie
scores. Then it returns `length` + 1 for each scores for tie scores
and the next rank.

Here's an example of custom strategy function that assigns no ranks to tie
scores:

::

   >>> def exclusive(start, length):
   ...     return [None] * length + [start]
   >>> list(Ranking([100, 80, 80, 70], exclusive))
   [(0, 100), (None, 80), (None, 80), (1, 70)]

Install
~~~~~~~

The package is available in `PyPI <http://pypi.python.org/pypi/ranking>`_. To
install it in your system, use `easy_install`:

.. sourcecode:: bash

   $ easy_install ranking

Or check out developement version:

.. sourcecode:: bash

   $ git clone git://github.com/sublee/ranking.git

Licensing and Author
~~~~~~~~~~~~~~~~~~~~

This project is licensed under BSD_. See LICENSE_ for the details.

I'm `Heungsub Lee`_, a game developer. Any regarding questions or patches are
welcomed.

.. _BSD: http://en.wikipedia.org/wiki/BSD_licenses
.. _LICENSE: https://github.com/sublee/ranking/blob/master/LICENSE
.. _Heungsub Lee: http://subl.ee/
