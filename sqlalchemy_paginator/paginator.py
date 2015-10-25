'''
Created on Oct 20, 2015

@author: ahmadjaved.se@gmail.com
'''
from math import ceil
from sqlalchemy import func

from exceptions import PageNotAnInteger, EmptyPage


class Paginator(object):
    """
    This class help you to manage data with pagination. This class will fetch
    data in pages. That is, instead of fetching all the records from database
    at a time, this class will fetch defined number of records at a time.
    
    So that you can perform particular action(s) on fetched data and then fetch
    data for next page. In this way we can get ride from the memory overloading
    problem as well.
    
    This class will optimized the query to fetch total number of records from
    database against given query_set. Optimization will applied only the query
    that will used to fetch records. You can also provide the separate query in
    optional_count_query_set that will used for count total records.
    """
    def __init__(self, query_set, per_page_limit, optional_count_query_set=None,
                 allow_empty_first_page=True):
        """
        Constructor to create the paginator object.
        
        :param query_set: SQLAlchemy query which is used for fetching data from
                          from database.
        :type query_set: SQLAlchemy query object. 
        :param per_page_limit: Required number of records in a page.
        :type per_page_limit: int.
        :param optional_count_query_set: This is a optional query set that will
                                         use to fetch the total number of
                                         records from database. If this optional
                                         query is not provided than this class
                                         will optimized query_set query and used
                                         that optimized query of getting total
                                         number of records from database.
        :type optional_count_query_set: SQLAlchemy query object.
        :param allow_empty_first_page: If this flag is true and there is no
                                       data in database against given query then
                                       it will return empty list on getting
                                       first page otherwise this will raise
                                       EmptyPage error. Default value of this
                                       parameter is true.
        :type allow_empty_first_page: bool.
        """
        self.query_set = query_set
        self.per_page_limit = per_page_limit
        self.optional_count_query_set = optional_count_query_set
        self.allow_empty_first_page = allow_empty_first_page
        self._total_pages = self._count = None

    def validate_page_number(self, page_number):
        """
        This method valid that if given page number is valid or not. Like page
        number should be integer and greater than zero and should not be greater
        than total number of pages.
        
        :param page_number: Required page number against which you want to fetch
                            records from database.
        :type page_number: int.
        :return: If given page number is valid then return it.
        :rtype: int.
        
        ..warning::
            This function can raise the following exceptions
            - PageNotAnInteger
            - EmptyPage
        """
        try:
            page_number = int(page_number)
        except ValueError:
            raise PageNotAnInteger('That page number is not an integer')
        if page_number < 1:
            raise EmptyPage('That page number is less than 1')
        if page_number > self.total_pages:
            if page_number == 1 and self.allow_empty_first_page:
                pass
            else:
                raise EmptyPage('That page contains no results')
        return page_number

    def page(self, page_number):
        """
        Returns a page object against given page number if given page number is
        valid.
        
        :param page_number: Required page number against which you want to fetch
                            records from database.
        :type page_number: int.
        :return: Page object that contains the records against given page 
                 number.
        :rtype: Page.
        
        ..seealso::
            - Page class
            - Paginator.validate_page_number()
        
        ..warning::
            This function can raise the following exceptions
            - PageNotAnInteger
            - EmptyPage
        """
        page_number = self.validate_page_number(page_number)
        offset = (page_number - 1) * self.per_page_limit
        return Page(self.query_set[offset, self.per_page_limit], page_number,
                    self)

    @property
    def count(self):
        """
        Returns the total number of objects, across all pages.
        
        :return: Total number of records against given query.
        :rtype: int.
        
        ..info::
            If optional_count_query_set is given then this function will use
            query for fetching total number records otherwise query_set query
            will be used for fetching total number records.
        """
        if self._count is None:
            if self.optional_count_query_set is None:
                self.count_query_set_optional = self.query_set.order_by(None)
            self._count = self.count_query_set_optional.with_entities(func.count('*')).scalar()
        return self._count

    @property
    def total_pages(self):
        """
        Returns the total number of pages.
        
        :return: Total number of pages against given query.
        :rtype: int.
        
        ..info::
            If total number of records is zero and allow_empty_first_page is
            true then returns 1 instead of 0.
        """
        ""
        if self._total_pages is None:
            if self.count == 0 and not self.allow_empty_first_page:
                self._total_pages = 0
            else:
                hits = max(1, self.count)
                self._total_pages = int(ceil(hits / float(self.per_page_limit)))
        return self._total_pages

    @property
    def pages_range(self):
        """
        Returns a range of pages.
        
        :return: List that contains range of pages.
        :rtype: list.
        """
        return range(1, self.total_pages + 1)


class Page(object):
    """
    This is a same copy of django Page class in paginator module. This class
    will be used in Paginator class for making pages. This Page class contains
    a list of objects of one page, page number and reference of paginator
    instance.
    """
    def __init__(self, object_list, number, paginator):
        self.object_list = object_list
        self.number = number
        self.paginator = paginator

    def __repr__(self):
        return '<Page %s of %s>' % (self.number, self.paginator.total_pages)

    def has_next(self):
        return self.number < self.paginator.total_pages

    def has_previous(self):
        return self.number > 1

    def has_other_pages(self):
        return self.has_previous() or self.has_next()

    def next_page_number(self):
        return self.number + 1

    def previous_page_number(self):
        return self.number - 1

    def start_index(self):
        """
        Returns the index of the first object on this page,
        relative to total objects in the paginator.
        """
        # Special case, return zero if no items.
        if self.paginator.count == 0:
            return 0
        return (self.paginator.per_page_limit * (self.number - 1)) + 1

    def end_index(self):
        """
        Returns the index of the last object on this page,
        relative to total objects found (hits).
        """
        # Special case for the last page
        if self.number == self.paginator.total_pages:
            return self.paginator.count
        return self.number * self.paginator.per_page_limit    
