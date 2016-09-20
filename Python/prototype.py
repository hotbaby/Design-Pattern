# -*- coding:utf-8 -*-

import copy
import logging
from collections import OrderedDict

_logger = logging.getLogger(__name__)


class Book(object):
    
    def __init__(self, name, authors, price, **attrs):
        self.name = name
        self.authors = authors
        self.price = price
        self.__dict__.update(**attrs)
        
    def __str__(self):
        l = []
        ordered = OrderedDict(sorted(self.__dict__.items()))
        for i in ordered.keys():
            l.append('{}:{}'.format(i, ordered[i]))
            if i == 'price':
                l.append('$')
            l.append('\n')
        return ''.join(l)
    

class Prototype(object):
    
    def __init__(self):
        self.objects = dict()
        
    def register(self, identifier, obj):
        self.objects[identifier] = obj
        
    def unregister(self, identifier):
        del self.objects[identifier]
        
    def clone(self, identifier, **attrs):
        found = self.objects.get(identifier)
        if not found:
            raise ValueError('Incorrect object identifier: {}'.format(identifier))
        new_obj = copy.deepcopy(found)
        new_obj.__dict__.update(**attrs)
        return new_obj


def main():
    book1 = Book('The C Programming Language',
                 ('Brian W. Kernighan', 'Dennis M.Ritchie'),
                 price=118,
                 publisher='Prentice Hall',
                 length=228,
                 publication_date='1978-02-22',
                 tags=('C', 'programming', 'algorithms', 'data structure'))
    prototype = Prototype()
    cid = 'k&r-first'
    prototype.register(cid, book1)
    
    book2 = prototype.clone(cid,
                            name='The C Programming Language(ANSI)',
                            price=48.99,
                            length=274,
                            publicate_date='1988-04-01',
                            edition=2)
    for book in (book1, book2):
        _logger.debug(book)