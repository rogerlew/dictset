# Copyright (c) 20[0,1,2][0,1,2], Roger Lew
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above
#     copyright notice, this list of conditions and the following
#     disclaimer in the documentation and/or other materials provided
#     with the distribution.
#   * Neither the name of the organizations affiliated with the
#     contributors or the names of its contributors themselves may be
#     used to endorse or promote products derived from this software
#     without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# This software is funded in part by NIH Grant NIH Grant P20 RR016454.

"""
This unittest tests the dictset module.
"""

import unittest
import doctest
import random

from test import test_support
from random import shuffle
from string import digits,ascii_lowercase

import dictset
from dictset import DictSet

# First we need to define some translator functions so we
# can compare DictSets without relying on DictSet itself.
#
# Comparisons are made as with sorted lists of key value
# pairs. The values (sets) are also sorted and turned into
# lists

def s2d(x=None):
    """
    s2d(...) -> takes a string returns a dict
        
        A shortcut function for turning strings into dicts
        with list values for testing dictset
        
        lowercase letters become keys,
        whole numbers become list elements,
        0 becomes an empty list
        all other characters are ignored

        s2d() -> {}
        s2d('') -> {}
        
        >>> s2d('a0b123c  567')
        {'a': [], 'c': ['5', '6', '7'], 'b': ['1', '2', '3']} 
    """
    if x==None or x=='': return {}
    
    keys,vals=[],[]

    for c in x:
        if c in ascii_lowercase:
            keys.append(c)
            vals.append([])
        elif c in '123456789':
            vals[-1]+=c
        #else c is '0' whitespace, non-alpha, etc.

    # randomly shuffle the order of the values in the list
    for v in vals:
        shuffle(v) # shuffles in place
            
    return dict(zip(keys,vals))

def d2l(ds):
    """
    s2l(...) -> takes a dict/DictSet returns sorted list of (k,v) pairs.
    
        takes a mappable. Sorts the item pairs, and and listifies
        and sorts the values
    """
    
    return [(k,sorted(list(v))) for (k,v) in sorted(ds.items())]

def s2l(x=None):
    """
    s2d(...) -> takes a string returns sorted list of (k,v) pairs.

        >>> s2d('b312a0c756')
        [('a', []), ('b', ['1', '2', '3']), ('c', ['5', '6', '7'])]
    """
    return d2l(s2d(x))

class TestDictSet__init__(unittest.TestCase):
    # Init test failure assertions
    def test0(self):
        with self.assertRaises(TypeError) as cm:
            DictSet(42)

        self.assertEqual(str(cm.exception),
                 "'int' object is not iterable")
        
    def test1(self):
        with self.assertRaises(TypeError) as cm:
            DictSet(one=1, two=2)

        self.assertEqual(str(cm.exception),
                 "'int' object is not iterable")
        
    def test2(self):
        with self.assertRaises(TypeError) as cm:
            DictSet([('one',1),('two',2)])

        self.assertEqual(str(cm.exception),
                 "'int' object is not iterable")
        
    def test3(self):
        with self.assertRaises(TypeError) as cm:
            DictSet(['one',[1],'two',[2]])

        self.assertEqual(str(cm.exception),
                 'could not unpack arg to key/value pairs')
        
    def test4(self):
        with self.assertRaises(TypeError) as cm:
            DictSet([('one'),[1],'two',[2]])

        self.assertEqual(str(cm.exception),
                'could not unpack arg to key/value pairs')
        
    def test5(self):
        with self.assertRaises(TypeError) as cm:
            DictSet([(set('one'),[1]),('two',[2])])

        self.assertEqual(str(cm.exception),
                 "unhashable type: 'set'")
        
    def test6(self):        
        with self.assertRaises(TypeError) as cm:
            DictSet([(set('one'),[1]),('two',[2])],{'three':[3]})

        self.assertEqual(str(cm.exception),
                 'DictSet expected at most 1 arguments, got 2')

    # test initialization signatures
    def test20(self):
        """DictSet()"""
        self.assertEqual(DictSet(),{})

    def test21(self):
        """DictSet(mapping)"""
        self.assertEqual(
            d2l(DictSet(s2d('a0b12333c45556'))),
                        s2l('a0b123  c45  6'))

    def test22(self):
        """DictSet(iterable)"""
        self.assertEqual(
            d2l(DictSet([('a',''),('b','123'),('c','45556'),])),
                      s2l('a  0     b   123     c   45  6'))

    def test23(self):
        """DictSet(**kwargs)"""
        self.assertEqual(
            d2l(DictSet(a='',b='123',c='45556')),
                   s2l('a 0  b  123  c  45  6'))

    def test24(self):
        """self can be a keyword)"""
        self.assertEqual(
            d2l(DictSet(self='45556')),
                  d2l({'self':'456'}))

    def test25(self):
        """DictSet(iterable, **kwargs), with overlapping key/values"""
        self.assertEqual(
            d2l(DictSet(s2d('a1c5678'),a='',b='123',c='456')),
                        s2l('a1             b  123  c  45678'))
                
    def test99(self):
        """Make sure that direct calls to update
           do not clear previous contents"""
        
        L=DictSet(a='1',b='2')
        L.__init__(b='3',c='4')
        self.assertEqual(d2l(L),s2l('a1b23c4'))

class TestDictSet_remove(unittest.TestCase):
    def test0(self):
        L = DictSet(s2d('a1 c5666788'))
        R =         s2l('a1 c56  7')
        L.remove('c','8')
        
        self.assertEqual(d2l(L),R)

    def test1(self):
        L = DictSet(s2d('a1 c5666788'))
        R =         s2l('a1 c56  7')
        L.remove('c','8')
        
        with self.assertRaises(KeyError) as cm:
            L.remove('c','8')

        self.assertEqual(str(cm.exception),"'8'")

    def test2(self):
        L = DictSet(s2d('a1 c5666788'))
        R =         s2l('a1 c56  7')
        L.remove('c','8')
        
        with self.assertRaises(KeyError) as cm:
            L.remove('d','8')

        self.assertEqual(str(cm.exception),"'d'")

    def test4(self):
        L = DictSet(s2d('a1 c5666788'))
        R =         s2l('a1 c56  7')
        L.remove('c','8')
        
        with self.assertRaises(TypeError) as cm:
            L.remove([],'8')

        self.assertEqual(str(cm.exception),
                "unhashable type: 'list'")

class TestDictSet_add(unittest.TestCase):
    def test0(self):
        L = DictSet(s2d('a1 c5666788'))
        R =         s2l('a1 c56  78 9')
        L.add('c','9') # add to existing set
        
        self.assertEqual(d2l(L),R)

    def test1(self):
        L = DictSet(s2d('a1 c5666788'))
        R =         s2l('a1 c56  78')
        L.add('c','7') # does nothing to existing set
        
        self.assertEqual(d2l(L),R)

    def test3(self):
        L = DictSet(s2d('a1 c5666788'))
        R =         s2l('a1 c56  78  d7')
        L.add('d','7') # create new set
        
        self.assertEqual(d2l(L),R)
        
    def test4(self):
        L = DictSet(s2d('a1 c5666788'))
        
        with self.assertRaises(TypeError) as cm:
            L.add('d',[])

        self.assertEqual(str(cm.exception),
                "unhashable type: 'list'")

    def test5(self):
        L = DictSet(s2d('a1 c5666788'))
        
        with self.assertRaises(TypeError) as cm:
            L.add([],'8')

        self.assertEqual(str(cm.exception),
                "unhashable type: 'list'")

class TestDictSet_copy(unittest.TestCase):
    def test0(self):
        L  = DictSet(s2d('a1 c5678'))
        R1 =         s2l('a1 c5678')
        M=L.copy()
        M.add('d','9')

        self.assertEqual(d2l(L),R1)

    def test1(self):
        L  = DictSet(s2d('a1 c5678'))
        M=L.copy()
        M.add('d','9')
        R2 =         s2l('a1 c5678 d9')

        self.assertEqual(d2l(M),R2)
        
class TestDictSet_discard(unittest.TestCase):
    def test0(self):
        L = DictSet(s2d('a1 c5666788'))
        R =         s2l('a1 c56  7')
        L.discard('c','8')
        
        self.assertEqual(d2l(L),R)

    def test1(self):
        L = DictSet(s2d('a1 c5666788'))
        R =         s2l('a1 c56  7')
        L.discard('c','8')
        L.discard('c','8') # doesn't raise KeyError

    def test2(self):
        L = DictSet(s2d('a1c5666788'))
        R =         s2l('a1c56  7')
        L.discard('d','8') # doesn't raise KeyError

    def test3(self):
        L = DictSet(s2d('a1 c5666788'))
        R =         s2l('a1 c56  7')
        
        with self.assertRaises(TypeError) as cm:
            L.discard([],'8')

        self.assertEqual(str(cm.exception),
                "unhashable type: 'list'")

class TestDictSet__setitem__(unittest.TestCase):
    def test0(self):
        L = DictSet(s2d('a1 c5666788'))
        R =         s2l('a1 c56  7')
        
        with self.assertRaises(TypeError) as cm:
            L.__setitem__([],'8')

        self.assertEqual(str(cm.exception),
                "unhashable type: 'list'")

    def test1(self):
        L = DictSet(s2d('a1 c5666788'))
        R =         s2l('a1 c56  7')
        
        with self.assertRaises(TypeError) as cm:
            L.__setitem__('a',42)

        self.assertEqual(str(cm.exception),
                "'int' object is not iterable")

    def test2(self):
        L = DictSet(s2d('a1 c5666788'))
        R =         s2l('a1 c42')
        
        L.__setitem__('c','42') # overwrite existing item
        self.assertEqual(d2l(L),R)

    def test3(self):
        L = DictSet(s2d('a1 c5666788'))
        R =         s2l('a1 c56  78  z42')
        
        L.__setitem__('z','42') # create new item
        self.assertEqual(d2l(L),R)       

class TestDictSet__setitem__(unittest.TestCase):
    def test0(self):
        L = DictSet(s2d('a1 c5666788'))
        R =         s2l('a1 c56  7')

class TestDictSet_get(unittest.TestCase):
    def test0(self):
        L = DictSet(s2d('a1 c5666788'))
        self.assertEqual(L.get('c'),set('5678')) 
        
    def test1(self):
        L = DictSet(s2d('a1 c5666788'))
        self.assertEqual(L.get('d'),None)

    def test2(self):
        L = DictSet(s2d('a1 c5666788'))
        R=          s2l('a1 c5678')
        
        self.assertEqual(L.get('d',[]),set())
        self.assertEqual(d2l(L),R)
        
    def test3(self):
        L = DictSet(s2d('a1 c5666788'))
        R=          s2l('a1 c5678')
        
        self.assertEqual(L.get('d','234'),set('234'))
        self.assertEqual(d2l(L),R)

class TestDictSet_setdefault(unittest.TestCase):
    def test0(self):
        L = DictSet(s2d('a1 c5666788'))
        self.assertEqual(L.setdefault('c'),set('5678')) 
        
    def test1(self):
        L = DictSet(s2d('a1 c5666788'))
        self.assertEqual(L.setdefault('d'),None)

    def test2(self):
        L = DictSet(s2d('a1 c5666788'))
        R=          s2l('a1 c5678    d0')
        
        self.assertEqual(L.setdefault('d',[]),set())
        self.assertEqual(d2l(L),R)
        
    def test3(self):
        L = DictSet(s2d('a1 c5666788'))
        R=          s2l('a1 c5678    d234')
        
        self.assertEqual(L.setdefault('d','234'),set('234'))
        self.assertEqual(d2l(L),R)
        
## update functions
class TestDictSet_update(unittest.TestCase):
    """update is a union update"""
    
    def test0(self):
        L = DictSet(s2d('a1c5666788'))
        M = DictSet(s2d(''))
        R =         s2l('a1c56  78')
        L.update(M)
        
        self.assertEqual(d2l(L),R) # L is updated
        self.assertEqual(d2l(M),M) # M is unchanged

    def test1(self):
        L = DictSet(s2d(''))
        M = DictSet(s2d('a1c5666788'))
        R =         s2l('a1c56  78')
        L.update(M)
        
        self.assertEqual(d2l(L),R) # L is updated
        self.assertEqual(d2l(M),M) # M is unchanged
        
    def test2(self):
        L = DictSet(s2d('a1        c5666788'))
        M = DictSet(s2d('a123 b324'))
        R =         s2l('a123 b324 c56  78')
        L.update(M)
        
        self.assertEqual(d2l(L),R) # L is updated
        self.assertEqual(d2l(M),M) # M is unchanged

    def test3(self):
        L = DictSet(s2d('a123 b324'))
        M = DictSet(s2d('a1        c5666788'))
        R =         s2l('a123 b324 c56  78')
        L.update(M)
        
        self.assertEqual(d2l(L),R) # L is updated
        self.assertEqual(d2l(M),M) # M is unchanged

## update functions
class TestDictSet__ior__(unittest.TestCase):
    """update is a union update"""
    
    def test0(self):
        L = DictSet(s2d('a1c5666788'))
        M = DictSet(s2d(''))
        R =         s2l('a1c56  78')
        L|=M
        
        self.assertEqual(d2l(L),R) # L is updated
        self.assertEqual(d2l(M),M) # M is unchanged

    def test1(self):
        L = DictSet(s2d(''))
        M = DictSet(s2d('a1c5666788'))
        R =         s2l('a1c56  78')
        L|=M
        
        self.assertEqual(d2l(L),R) # L is updated
        self.assertEqual(d2l(M),M) # M is unchanged
        
    def test2(self):
        L = DictSet(s2d('a1        c5666788'))
        M = DictSet(s2d('a123 b324'))
        R =         s2l('a123 b324 c56  78')
        L|=M
        
        self.assertEqual(d2l(L),R) # L is updated
        self.assertEqual(d2l(M),M) # M is unchanged

    def test3(self):
        L = DictSet(s2d('a123 b324'))
        M = DictSet(s2d('a1        c5666788'))
        R =         s2l('a123 b324 c56  78')
        L|=M
        
        self.assertEqual(d2l(L),R) # L is updated
        self.assertEqual(d2l(M),M) # M is unchanged
        
class TestDictSet_difference_update(unittest.TestCase):
    """update is a difference update"""
    
    def test0(self):
        L = DictSet(s2d('a1 c5666788'))
        M = DictSet(s2d(''))
        R =         s2l('a1 c56  78')
        L.difference_update(M)
        
        self.assertEqual(d2l(L),R) # L is updated
        self.assertEqual(d2l(M),M) # M is unchanged

    def test1(self):
        L = DictSet(s2d(''))
        M = DictSet(s2d('a1 c5666788'))
        R =         s2l('')
        L.difference_update(M)
        
        self.assertEqual(d2l(L),R) # L is updated
        self.assertEqual(d2l(M),M) # M is unchanged
        
    def test2(self):
        L = DictSet(s2d('a1        c56788'))
        M = DictSet(s2d('a123 b324 c5 78'))
        R =         s2l('          c 6')
        L.difference_update(M)
        
        self.assertEqual(d2l(L),R) # L is updated
        self.assertEqual(d2l(M),M) # M is unchanged

    def test3(self):
        L = DictSet(s2d('a123 b324 c5 78'))
        M = DictSet(s2d('a1        c56788'))
        R =         s2l('a 23 b324')
        L.difference_update(M)
        
        self.assertEqual(d2l(L),R) # L is updated
        self.assertEqual(d2l(M),M) # M is unchanged

class TestDictSet__isub__(unittest.TestCase):
    """update is a difference update"""
    
    def test0(self):
        L = DictSet(s2d('a1 c5666788'))
        M = DictSet(s2d(''))
        R =         s2l('a1 c56  78')
        L-=M
        
        self.assertEqual(d2l(L),R) # L is updated
        self.assertEqual(d2l(M),M) # M is unchanged

    def test1(self):
        L = DictSet(s2d(''))
        M = DictSet(s2d('a1 c5666788'))
        R =         s2l('')
        L-=M
        
        self.assertEqual(d2l(L),R) # L is updated
        self.assertEqual(d2l(M),M) # M is unchanged
        
    def test2(self):
        L = DictSet(s2d('a1        c56788'))
        M = DictSet(s2d('a123 b324 c5 78'))
        R =         s2l('          c 6')
        L-=M
        
        self.assertEqual(d2l(L),R) # L is updated
        self.assertEqual(d2l(M),M) # M is unchanged

    def test3(self):
        L = DictSet(s2d('a123 b324 c5 78'))
        M = DictSet(s2d('a1        c56788'))
        R =         s2l('a 23 b324')
        L-=M
        
        self.assertEqual(d2l(L),R) # L is updated
        self.assertEqual(d2l(M),M) # M is unchanged

class TestDictSet_symmetric_difference_update(unittest.TestCase):
    """tests symmetric_difference_update"""
    
    def test0(self):
        L = DictSet(s2d('a1 c5666788'))
        M = DictSet(s2d(''))
        R =         s2l('a1 c56  78')
        L.symmetric_difference_update(M)
        
        self.assertEqual(d2l(L),R) # L is updated
        self.assertEqual(d2l(M),M) # M is unchanged

    def test1(self):
        L = DictSet(s2d(''))
        M = DictSet(s2d('a1 c5666788'))
        R =         s2l('a1 c56  78')
        L.symmetric_difference_update(M)
        
        self.assertEqual(d2l(L),R) # L is updated
        self.assertEqual(d2l(M),M) # M is unchanged
        
    def test2(self):
        L = DictSet(s2d('a1        c56788'))
        M = DictSet(s2d('a123 b324 c5 78'))
        R =         s2l('a 23 b324 c 6')
        L.symmetric_difference_update(M)
        
        self.assertEqual(d2l(L),R) # L is updated
        self.assertEqual(d2l(M),M) # M is unchanged

    def test3(self):
        L = DictSet(s2d('a123 b324 c5 78'))
        M = DictSet(s2d('a1        c56788'))
        R =         s2l('a 23 b324 c 6')
        L.symmetric_difference_update(M)
        
        self.assertEqual(d2l(L),R) # L is updated
        self.assertEqual(d2l(M),M) # M is unchanged

class TestDictSet__ixor__(unittest.TestCase):
    """test symmetric_difference_update overloading"""
    
    def test0(self):
        L = DictSet(s2d('a1 c5666788'))
        M = DictSet(s2d(''))
        R =         s2l('a1 c56  78')
        L^=M
        
        self.assertEqual(d2l(L),R) # L is updated
        self.assertEqual(d2l(M),M) # M is unchanged

    def test1(self):
        L = DictSet(s2d(''))
        M = DictSet(s2d('a1 c5666788'))
        R =         s2l('a1 c56  78')
        L^=M
        
        self.assertEqual(d2l(L),R) # L is updated
        self.assertEqual(d2l(M),M) # M is unchanged
        
    def test2(self):
        L = DictSet(s2d('a1        c56788'))
        M = DictSet(s2d('a123 b324 c5 78'))
        R =         s2l('a 23 b324 c 6')
        L^=M
        
        self.assertEqual(d2l(L),R) # L is updated
        self.assertEqual(d2l(M),M) # M is unchanged

    def test3(self):
        L = DictSet(s2d('a123 b324 c5 78'))
        M = DictSet(s2d('a1        c56788'))
        R =         s2l('a 23 b324 c 6')
        L^=M
        
        self.assertEqual(d2l(L),R) # L is updated
        self.assertEqual(d2l(M),M) # M is unchanged

class TestDictSet_intersection_update(unittest.TestCase):
    """tests intersection_update"""
    
    def test0(self):
        L = DictSet(s2d('a1 c5666788'))
        M = DictSet(s2d(''))
        R =         s2l('')
        L.intersection_update(M)
        
        self.assertEqual(d2l(L),R) # L is updated
        self.assertEqual(d2l(M),M) # M is unchanged

    def test1(self):
        L = DictSet(s2d(''))
        M = DictSet(s2d('a1 c5666788'))
        R =         s2l('')
        L.intersection_update(M)
        
        self.assertEqual(d2l(L),R) # L is updated
        self.assertEqual(d2l(M),M) # M is unchanged
        
    def test2(self):
        L = DictSet(s2d('a1        c567889'))
        M = DictSet(s2d('a123 b324 c5 78'))
        R =         s2l('a1        c5 78 ')
        L.intersection_update(M)
        
        self.assertEqual(d2l(L),R) # L is updated
        self.assertEqual(d2l(M),M) # M is unchanged

    def test3(self):
        L = DictSet(s2d('a123 b324 c5 78'))
        M = DictSet(s2d('a1        c567889'))
        R =         s2l('a1        c5 78 ')
        L.intersection_update(M)
        
        self.assertEqual(d2l(L),R) # L is updated
        self.assertEqual(d2l(M),M) # M is unchanged

class TestDictSet__iand__(unittest.TestCase):
    """test intersection_update overloading"""
    
    def test0(self):
        L = DictSet(s2d('a1 c5666788'))
        M = DictSet(s2d(''))
        R =         s2l('')
        L&=M
        
        self.assertEqual(d2l(L),R) # L is updated
        self.assertEqual(d2l(M),M) # M is unchanged

    def test1(self):
        L = DictSet(s2d(''))
        M = DictSet(s2d('a1 c5666788'))
        R =         s2l('')
        L&=M
        
        self.assertEqual(d2l(L),R) # L is updated
        self.assertEqual(d2l(M),M) # M is unchanged
        
    def test2(self):
        L = DictSet(s2d('a1        c56788'))
        M = DictSet(s2d('a123 b324 c5 78'))
        R =         s2l('a1        c5 78')
        L&=M
        
        self.assertEqual(d2l(L),R) # L is updated
        self.assertEqual(d2l(M),M) # M is unchanged

    def test3(self):
        L = DictSet(s2d('a123 b324 c5 78'))
        M = DictSet(s2d('a1        c56788'))
        R =         s2l('a1        c5 78')
        L&=M
        
        self.assertEqual(d2l(L),R) # L is updated
        self.assertEqual(d2l(M),M) # M is unchanged
        
# set operations
class TestDictSet_union(unittest.TestCase):
    """update is a union update"""
    
    def test0(self):
        L = DictSet(s2d('a1c5666788'))
        M = DictSet(s2d(''))
        R =         s2l('a1c56  78')
        
        self.assertEqual(d2l(L.union(M)),R) 
        self.assertEqual(d2l(L),L) # L is unchanged
        self.assertEqual(d2l(M),M) # M is unchanged

    def test1(self):
        L = DictSet(s2d(''))
        M = DictSet(s2d('a1c5666788'))
        R =         s2l('a1c56  78')

        self.assertEqual(d2l(L.union(M)),R)
        self.assertEqual(d2l(L),L) # L is unchanged
        self.assertEqual(d2l(M),M) # M is unchanged
        
    def test2(self):
        L = DictSet(s2d('a1        c5666788'))
        M = DictSet(s2d('a123 b324'))
        R =         s2l('a123 b324 c56  78')

        self.assertEqual(d2l(L.union(M)),R)
        self.assertEqual(d2l(L),L) # L is unchanged
        self.assertEqual(d2l(M),M) # M is unchanged

    def test3(self):
        L = DictSet(s2d('a123 b324'))
        M = DictSet(s2d('a1        c5666788'))
        R =         s2l('a123 b324 c56  78')

        self.assertEqual(d2l(L.union(M)),R)
        self.assertEqual(d2l(L),L) # L is unchanged
        self.assertEqual(d2l(M),M) # M is unchanged

class TestDictSet__or__(unittest.TestCase):
    """update is a union update"""
    
    def test0(self):
        L = DictSet(s2d('a1c5666788'))
        M = DictSet(s2d(''))
        R =         s2l('a1c56  78')
        
        self.assertEqual(d2l(L|M),R) 
        self.assertEqual(d2l(L),L) # L is unchanged
        self.assertEqual(d2l(M),M) # M is unchanged

    def test1(self):
        L = DictSet(s2d(''))
        M = DictSet(s2d('a1c5666788'))
        R =         s2l('a1c56  78')

        self.assertEqual(d2l(L|M),R)
        self.assertEqual(d2l(L),L) # L is unchanged
        self.assertEqual(d2l(M),M) # M is unchanged
        
    def test2(self):
        L = DictSet(s2d('a1        c5666788'))
        M = DictSet(s2d('a123 b324'))
        R =         s2l('a123 b324 c56  78')

        self.assertEqual(d2l(L|M),R)
        self.assertEqual(d2l(L),L) # L is unchanged
        self.assertEqual(d2l(M),M) # M is unchanged

    def test3(self):
        L = DictSet(s2d('a123 b324'))
        M = DictSet(s2d('a1        c5666788'))
        R =         s2l('a123 b324 c56  78')

        self.assertEqual(d2l(L|M),R)
        self.assertEqual(d2l(L),L) # L is unchanged
        self.assertEqual(d2l(M),M) # M is unchanged

class TestDictSet_difference(unittest.TestCase):
    """update is a union update"""
    
    def test0(self):
        L = DictSet(s2d('a1 c5666788'))
        M = DictSet(s2d(''))
        R =         s2l('a1 c56  78')

        self.assertEqual(d2l(L.difference(M)),R)
        self.assertEqual(d2l(L),L) # L is unchanged
        self.assertEqual(d2l(M),M) # M is unchanged

    def test1(self):
        L = DictSet(s2d(''))
        M = DictSet(s2d('a1 c5666788'))
        R =         s2l('')

        self.assertEqual(d2l(L.difference(M)),R)
        self.assertEqual(d2l(L),L) # L is unchanged
        self.assertEqual(d2l(M),M) # M is unchanged
        
    def test2(self):
        L = DictSet(s2d('a1        c56788'))
        M = DictSet(s2d('a123 b324 c5 78'))
        R =         s2l('          c 6')

        self.assertEqual(d2l(L.difference(M)),R)
        self.assertEqual(d2l(L),L) # L is unchanged
        self.assertEqual(d2l(M),M) # M is unchanged

    def test3(self):
        L = DictSet(s2d('a123 b324 c5 78'))
        M = DictSet(s2d('a1        c56788'))
        R =         s2l('a 23 b324')

        self.assertEqual(d2l(L.difference(M)),R)
        self.assertEqual(d2l(L),L) # L is unchanged
        self.assertEqual(d2l(M),M) # M is unchanged
        
class TestDictSet__sub__(unittest.TestCase):
    """update is a union update"""
    
    def test0(self):
        L = DictSet(s2d('a1 c5666788 e0'))
        M = DictSet(s2d(''))
        R =         s2l('a1 c56  78')

        self.assertEqual(d2l(L-M),R)
        self.assertEqual(d2l(L),L) # L is unchanged
        self.assertEqual(d2l(M),M) # M is unchanged

    def test1(self):
        L = DictSet(s2d(''))
        M = DictSet(s2d('a1 c5666788 e0'))
        R =         s2l('')

        self.assertEqual(d2l(L-M),R)
        self.assertEqual(d2l(L),L) # L is unchanged
        self.assertEqual(d2l(M),M) # M is unchanged
        
    def test2(self):
        L = DictSet(s2d('a1        c56788 e0'))
        M = DictSet(s2d('a123 b324 c5 78 d0'))
        R =         s2l('          c 6')

        self.assertEqual(d2l(L-M),R)
        self.assertEqual(d2l(L),L) # L is unchanged
        self.assertEqual(d2l(M),M) # M is unchanged

    def test3(self):
        L = DictSet(s2d('a123 b324 c5 78 d0'))
        M = DictSet(s2d('a1        c56788 e0'))
        R =         s2l('a 23 b324')

        self.assertEqual(d2l(L-M),R)
        self.assertEqual(d2l(L),L) # L is unchanged
        self.assertEqual(d2l(M),M) # M is unchanged

class TestDictSet_symmetric_difference(unittest.TestCase):
    def test0(self):
        L = DictSet(s2d('a1 c5666788 e0'))
        M = DictSet(s2d(''))
        R =         s2l('a1 c56  78')

        self.assertEqual(d2l(L.symmetric_difference(M)),R)
        self.assertEqual(d2l(L),L) # L is unchanged
        self.assertEqual(d2l(M),M) # M is unchanged

    def test1(self):
        L = DictSet(s2d(''))
        M = DictSet(s2d('a1 c5666788 e0'))
        R =         s2l('a1 c56  78')

        self.assertEqual(d2l(L.symmetric_difference(M)),R)
        self.assertEqual(d2l(L),L) # L is unchanged
        self.assertEqual(d2l(M),M) # M is unchanged
        
    def test2(self):
        L = DictSet(s2d('a1        c56788 e0'))
        M = DictSet(s2d('a123 b324 c5 78 d0'))
        R =         s2l('a 23 b324 c 6')

        self.assertEqual(d2l(L.symmetric_difference(M)),R)
        self.assertEqual(d2l(L),L) # L is unchanged
        self.assertEqual(d2l(M),M) # M is unchanged

    def test3(self):
        L = DictSet(s2d('a123 b324 c5 78 d0'))
        M = DictSet(s2d('a1        c56788 e0'))
        R =         s2l('a 23 b324 c 6')

        self.assertEqual(d2l(L.symmetric_difference(M)),R)
        self.assertEqual(d2l(L),L) # L is unchanged
        self.assertEqual(d2l(M),M) # M is unchanged

class TestDictSet__xor__(unittest.TestCase):
    def test0(self):
        L = DictSet(s2d('a1 c5666788 e0'))
        M = DictSet(s2d(''))
        R =         s2l('a1 c56  78')

        self.assertEqual(d2l(L^M),R)
        self.assertEqual(d2l(L),L) # L is unchanged
        self.assertEqual(d2l(M),M) # M is unchanged

    def test1(self):
        L = DictSet(s2d(''))
        M = DictSet(s2d('a1 c5666788 e0'))
        R =         s2l('a1 c56  78')

        self.assertEqual(d2l(L^M),R)
        self.assertEqual(d2l(L),L) # L is unchanged
        self.assertEqual(d2l(M),M) # M is unchanged
        
    def test2(self):
        L = DictSet(s2d('a1        c56788 e0'))
        M = DictSet(s2d('a123 b324 c5 78 d0'))
        R =         s2l('a 23 b324 c 6')

        self.assertEqual(d2l(L^M),R)
        self.assertEqual(d2l(L),L) # L is unchanged
        self.assertEqual(d2l(M),M) # M is unchanged

    def test3(self):
        L = DictSet(s2d('a123 b324 c5 78 d0'))
        M = DictSet(s2d('a1        c56788 e0'))
        R =         s2l('a 23 b324 c 6')

        self.assertEqual(d2l(L^M),R)
        self.assertEqual(d2l(L),L) # L is unchanged
        self.assertEqual(d2l(M),M) # M is unchanged

class TestDictSet_intersection(unittest.TestCase):
    def test0(self):
        L = DictSet(s2d('a1 c5666788'))
        M = DictSet(s2d(''))
        R =         s2l('')

        self.assertEqual(d2l(L.intersection(M)),R)
        self.assertEqual(d2l(L),L) # L is unchanged
        self.assertEqual(d2l(M),M) # M is unchanged

    def test1(self):
        L = DictSet(s2d(''))
        M = DictSet(s2d('a1 c5666788'))
        R =         s2l('')

        self.assertEqual(d2l(L.intersection(M)),R)
        self.assertEqual(d2l(L),L) # L is unchanged
        self.assertEqual(d2l(M),M) # M is unchanged
        
    def test2(self):
        L = DictSet(s2d('a1        c567889'))
        M = DictSet(s2d('a123 b324 c5 78'))
        R =         s2l('a1        c5 78 ')

        self.assertEqual(d2l(L.intersection(M)),R)
        self.assertEqual(d2l(L),L) # L is unchanged
        self.assertEqual(d2l(M),M) # M is unchanged

    def test3(self):
        L = DictSet(s2d('a123 b324 c5 78'))
        M = DictSet(s2d('a1        c567889'))
        R =         s2l('a1        c5 78 ')

        self.assertEqual(d2l(L.intersection(M)),R)
        self.assertEqual(d2l(L),L) # L is unchanged
        self.assertEqual(d2l(M),M) # M is unchanged

class TestDictSet__and__(unittest.TestCase):
    def test0(self):
        L = DictSet(s2d('a1 c5666788'))
        M = DictSet(s2d('e0'))
        R =         s2l('')

        self.assertEqual(d2l(L&M),R)
        self.assertEqual(d2l(L),L) # L is unchanged
        self.assertEqual(d2l(M),M) # M is unchanged

    def test1(self):
        L = DictSet(s2d(''))
        M = DictSet(s2d('a1 c5666788 d0'))
        R =         s2l('')

        self.assertEqual(d2l(L&M),R)
        self.assertEqual(d2l(L),L) # L is unchanged
        self.assertEqual(d2l(M),M) # M is unchanged
        
    def test2(self):
        L = DictSet(s2d('a1        c567889 d0'))
        M = DictSet(s2d('a123 b324 c5 78'))
        R =         s2l('a1        c5 78 ')

        self.assertEqual(d2l(L&M),R)
        self.assertEqual(d2l(L),L) # L is unchanged
        self.assertEqual(d2l(M),M) # M is unchanged

    def test3(self):
        L = DictSet(s2d('a123 b324 c5 78 e0'))
        M = DictSet(s2d('a1        c567889 d0'))
        R =         s2l('a1        c5 78 ')

        self.assertEqual(d2l(L&M),R)
        self.assertEqual(d2l(L),L) # L is unchanged
        self.assertEqual(d2l(M),M) # M is unchanged
        
# truth comparisons

class TestDictSet__eq__(unittest.TestCase):
    def test0(self):
        L = DictSet(s2d('a1 c5666788'))
        M = []
        self.assertFalse(L.__eq__(M))

    def test1(self):
        L = DictSet(s2d(''))
        M = 42
        self.assertFalse(L.__eq__(M))

    def test3(self):
        L = DictSet(s2d('a1b12345'))
        M = [('a','1'),('b','52341231425'),('c','')]
        self.assertTrue(L.__eq__(M))

    def test4(self):
        L = DictSet(s2d('a1b12345d0'))
        M = [('a','1'),('b','52341231425')]
        self.assertTrue(L.__eq__(M))

    def test5(self):
        L = DictSet()
        M = {}
        self.assertTrue(L.__eq__(M))

class TestDictSet__ne__(unittest.TestCase):
    def test0(self):
        L = DictSet(s2d('a1 c5666788'))
        M = []
        self.assertTrue(L.__ne__(M))

    def test1(self):
        L = DictSet(s2d(''))
        M = 42
        self.assertTrue(L.__ne__(M))

    def test3(self):
        L = DictSet(s2d('a1b12345'))
        M = [('a','1'),('b','52341231425'),('c','')]
        self.assertFalse(L.__ne__(M))

    def test4(self):
        L = DictSet(s2d('a1b12345d0'))
        M = [('a','1'),('b','52341231425')]
        self.assertFalse(L.__ne__(M))

    def test5(self):
        L = DictSet()
        M = {}
        self.assertFalse(L.__ne__(M))

class TestDictSet_issubset(unittest.TestCase):
    def test0(self):
        L = DictSet()
        M = s2d('a1 c5666788')
        self.assertTrue(L.issubset(M))

    def test1(self):
        with self.assertRaises(TypeError) as cm:
            DictSet().issubset(4)

        self.assertEqual(str(cm.exception),
                 "'int' object is not iterable")
        
    def test3(self):
        L = DictSet(s2d('a0b12345'))
        M = [('a','1'),('b','52341231425'),('c','')]
        self.assertTrue(L.issubset(M))

    def test31(self):
        L = DictSet([('a','1'),('b','52341231425'),('c','')])
        M = DictSet(s2d('a0b12345'))
        self.assertFalse(L.issubset(M))
        
    def test4(self):
        L = DictSet(s2d('a1b1234d0'))
        M = [('a','1'),('b','52341231425')]
        self.assertTrue(L.issubset(M))

    def test5(self):
        L = DictSet()
        M = {}
        self.assertTrue(L.issubset(M))

    def test6(self):
        L = DictSet(s2d('a0'))
        M = {}
        self.assertTrue(L.issubset(M))

class TestDictSet__le__(unittest.TestCase):
    def test0(self):
        L = DictSet()
        M = s2d('a1 c5666788')
        self.assertTrue(L<=M)

    def test1(self):
        with self.assertRaises(TypeError) as cm:
            DictSet().issubset(4)

        self.assertEqual(str(cm.exception),
                 "'int' object is not iterable")
        
    def test3(self):
        L = DictSet(s2d('a0b12345'))
        M = [('a','1'),('b','52341231425'),('c','')]
        self.assertTrue(L<=M)

    def test31(self):
        L = DictSet([('a','1'),('b','52341231425'),('c','')])
        M = DictSet(s2d('a0b12345'))
        self.assertFalse(L<=M)
        
    def test4(self):
        L = DictSet(s2d('a1b1234d0'))
        M = [('a','1'),('b','52341231425')]
        self.assertTrue(L<=M)

    def test5(self):
        L = DictSet()
        M = {}
        self.assertTrue(L<=M)

    def test6(self):
        L = DictSet(s2d('a0'))
        M = {}
        self.assertTrue(L<=M)
        
class TestDictSet_issuperset(unittest.TestCase):
    def test0(self):
        L = DictSet()
        M = s2d('a1 c5666788')
        self.assertFalse(L.issuperset(M))

    def test1(self):
        with self.assertRaises(TypeError) as cm:
            DictSet().issuperset(4)

        self.assertEqual(str(cm.exception),
                 "'int' object is not iterable")
        
    def test3(self):
        L = DictSet(s2d('a0b12345'))
        M = [('a','1'),('b','52341231425'),('c','')]
        self.assertFalse(L.issuperset(M))

    def test31(self):
        L = DictSet([('a','1'),('b','52341231425'),('c','')])
        M = DictSet(s2d('a0b12345'))
        self.assertTrue(L.issuperset(M))
        
    def test4(self):
        L = DictSet(s2d('a1b1234d0'))
        M = [('a','1'),('b','52341231425')]
        self.assertFalse(L.issuperset(M))

    def test5(self):
        L = DictSet()
        M = {}
        self.assertTrue(L.issuperset(M))

    def test6(self):
        L = DictSet(s2d('a0'))
        M = {}
        self.assertTrue(L.issuperset(M))

class TestDictSet__ge__(unittest.TestCase):
    def test0(self):
        L = DictSet()
        M = s2d('a1 c5666788')
        self.assertFalse(L>=M)

    def test1(self):
        with self.assertRaises(TypeError) as cm:
            DictSet().issuperset(4)

        self.assertEqual(str(cm.exception),
                 "'int' object is not iterable")
        
    def test3(self):
        L = DictSet(s2d('a0b12345'))
        M = [('a','1'),('b','52341231425'),('c','')]
        self.assertFalse(L>=M)

    def test31(self):
        L = DictSet([('a','1'),('b','52341231425'),('c','')])
        M = DictSet(s2d('a0b12345'))
        self.assertTrue(L>=M)
        
    def test4(self):
        L = DictSet(s2d('a1b1234d0'))
        M = [('a','1'),('b','52341231425')]
        self.assertFalse(L>=M)

    def test5(self):
        L = DictSet()
        M = {}
        self.assertTrue(L>=M)

    def test6(self):
        L = DictSet(s2d('a0'))
        M = {}
        self.assertTrue(L>=M)

class TestDictSet__contains__(unittest.TestCase):
    def test0(self):
        L = DictSet(s2d('a1 c5666788'))
        
        with self.assertRaises(TypeError) as cm:
            set() in L # set is an unhashable type

        self.assertEqual(str(cm.exception),
                 "unhashable type: 'set'")

    def test1(self):
        L = DictSet(s2d('a1 c5666788 d0'))
        self.assertTrue('a' in L)

    def test2(self):
        L = DictSet(s2d('a1 c5666788 d0'))
        self.assertFalse('d' in L) # d is a key, but has an empty set

    def test3(self):
        L = DictSet(s2d('a1 c5666788 d0'))
        self.assertFalse('e' in L) # really not a key

        
def suite():
    return unittest.TestSuite((
                unittest.makeSuite(TestDictSet__init__),
                unittest.makeSuite(TestDictSet_remove),
                unittest.makeSuite(TestDictSet_discard),
                unittest.makeSuite(TestDictSet_add),
                unittest.makeSuite(TestDictSet_get),
                unittest.makeSuite(TestDictSet_setdefault),
                unittest.makeSuite(TestDictSet_copy),
                unittest.makeSuite(TestDictSet__setitem__),
                unittest.makeSuite(TestDictSet_update),
                unittest.makeSuite(TestDictSet__ior__),
                unittest.makeSuite(TestDictSet_difference_update),
                unittest.makeSuite(TestDictSet__isub__),
                unittest.makeSuite(TestDictSet_symmetric_difference_update),
                unittest.makeSuite(TestDictSet__ixor__),
                unittest.makeSuite(TestDictSet_intersection_update),
                unittest.makeSuite(TestDictSet__iand__),
                unittest.makeSuite(TestDictSet_union),
                unittest.makeSuite(TestDictSet__or__),
                unittest.makeSuite(TestDictSet_difference),
                unittest.makeSuite(TestDictSet__sub__),
                unittest.makeSuite(TestDictSet_symmetric_difference),
                unittest.makeSuite(TestDictSet__xor__),
                unittest.makeSuite(TestDictSet_intersection),
                unittest.makeSuite(TestDictSet__and__),
                unittest.makeSuite(TestDictSet__eq__),
                unittest.makeSuite(TestDictSet__ne__),
                unittest.makeSuite(TestDictSet_issubset),
                unittest.makeSuite(TestDictSet__le__),
                unittest.makeSuite(TestDictSet_issuperset),
                unittest.makeSuite(TestDictSet__ge__),
                unittest.makeSuite(TestDictSet__contains__),
                              ))

if __name__ == "__main__":
    # run tests
    runner = unittest.TextTestRunner()
    runner.run(suite())
    
