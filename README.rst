.. image:: https://badge.fury.io/py/Sqlalchemy-paginator.svg
    :target: https://pypi.python.org/pypi/SQLAlchemy-Paginator
    :alt: PyPI Version

.. image:: https://img.shields.io/pypi/dm/SQLAlchemy-Paginator.svg
    :target: https://pypi.python.org/pypi/SQLAlchemy-Paginator
    :alt: PyPI Downloads

SQLAlchemy-Paginator
====================
This module helps you to manage large data with pagination.

How this module work?
---------------------
This module ``sqlalchemy_paginator.Paginator`` take an SQLAlchemy query - e.g.: ``Session.query(MyModel)`` and on calling page for specific page number it will fetch only required records from database instead of fetching all the records.

This class will also optimized the query for fetching total number of records from database against given query_set. Optimization will be applied only on the query that will be used for fetching total number of records. You can also provide the separate query in optional_count_query_set argument for fetching total number of records.

Usage
-----
You can use this paginator module in python scripting code and in web based application code as well.
    
**Example1**

::

  > from sqlalchemy_paginator import Paginator
  > query = session.query(MyModel)
  > paginator = Paginator(query, 5)
  > for page in paginator:
  >     print "page number of current page in iterator", page.number
  >     print "this is a list that contains the records of current page", page.object_list

**Example2**

::

  > from sqlalchemy_paginator import Paginator
  > query = session.query(MyModel)
  > paginator = Paginator(query, 5)
  > page = paginator.page(page_number)
  > print "to get total number of records against given query", page.paginator.count
  > print "to get total number of pages", page.paginator.total_pages
  > print "to get range of pages in list", page.paginator.pages_range
  > print "to get index of the first object on this page", page.start_index
  > print "to get index of the last object on this page", page.end_index
  > if page.has_previous():
  >     print "to get previous page number", page.previous_page_number
  > if page.has_next():
  >     print "to next previous page number", page.next_page_number

How to install?
---------------
When ``pip`` is available, the distribution can be downloaded from PyPI and installed in single step

::

  > pip install SQLAlchemy-Paginator

or you can use ``easy_install``

::

  > easy_install SQLAlchemy-Paginator

You can find more document in ``sqlalchemy_paginator/paginator.py`` module and a complete example in the ``tests/sqlalchemy_paginator_tests.py`` file of this Python module.
