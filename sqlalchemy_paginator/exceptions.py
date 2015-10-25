'''
Created on Oct 20, 2015

@author: ahmadjaved.se@gmail.com
'''

class InvalidPage(Exception):
    pass

class PageNotAnInteger(InvalidPage):
    pass

class EmptyPage(InvalidPage):
    pass