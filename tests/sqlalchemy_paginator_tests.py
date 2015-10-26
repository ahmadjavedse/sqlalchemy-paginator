"""
Created on Oct 22, 2015

@author: ahmadjaved.se@gmail.com
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import session
import unittest

from sqlalchemy_paginator import Paginator


class SQLAlchemyPaginatorTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:', echo=False)
        Base = declarative_base()
        from sqlalchemy import Column, Integer, String
        
        class Person(Base):
            __tablename__ = 'person'
            id = Column(Integer, primary_key=True)
            name = Column(String)
            
        Base.metadata.create_all(self.engine)
        
        Session = session.sessionmaker(bind=self.engine)
        self.session = Session()
        
        for i in range(1000):
            person = Person()
            person.name = i
            self.session.add(person)
            
        self.session.commit()
        
        self.Person = Person

    def test_pagination(self):
        query = self.session.query(self.Person)
        paginator = Paginator(query, 10)
        page = paginator.page(2)
        self.assertEquals(paginator.total_pages, 100, 
                          msg="Total page= %s, expected= %s" % (paginator.total_pages, 100))
        self.assertEquals(paginator.count, 1000, 
                          msg="Total records= %s, expected= %s" % (paginator.count, 1000))
        self.assertEquals(len(page.object_list), 10, 
                          msg="Total records in page= %s, expected= %s" % (len(page.object_list), 10))
        self.assertEquals(page.previous_page_number, 1, 
                          msg="Previous page number= %s, expected= %s" % (page.previous_page_number, 1))
        self.assertEquals(page.next_page_number, 3, 
                          msg="Next page number= %s, expected= %s" % (page.next_page_number, 3))
        self.assertEquals(page.start_index, 11, 
                          msg="Start index of page= %s, expected= %s" % (page.start_index, 11))
        self.assertEquals(page.end_index, 20, 
                          msg="End index of page= %s, expected= %s" % (page.end_index, 20))


if __name__ == '__main__':
    unittest.main()