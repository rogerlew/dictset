# Copyright (c) 2011, Roger Lew
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
# This software is funded in part by NIH Grant P20 RR016454.
#
__version__="0.99"

from copy import copy, deepcopy

class DictSet(dict):
    """
    DictSet() -> new empty dictionary of sets
    DictSet(mapping) -> new dictionary of sets initialized from a
        mapping object's (key, value) pairs
    DictSet(iterable) -> new dictionary of sets initialized as if via:
        d = {}
        for k, v in iterable:
            d[k] = set(v)
    DictSet(**kwargs) -> new dictionary of sets initialized with the
        name=value pairs in the keyword argument list.
        For example:  dict(one=[1], two=[2])
    
    A dict of sets that behaves like a set.

    """
    def __init__(*args, **kwds): # args[0] -> 'self'
        """
        Initialize DictSet

          Signature is the same as for regular dictionaries
        
            >>> DictSet()
            {}
            
            >>> DictSet(one=[1],two=[2])
            {'two': set([2]), 'one': set([1])}

            >>> DictSet([('one',[1]),('two',[2])])
            {'two': set([2]), 'one': set([1])}

            >>> DictSet({'one':[1],'two':[2]})
            {'two': set([2]), 'one': set([1])}

            >>> DictSet({'one':[1],'two':[2]},three=[3],four=[4])
            {'four': set([4]), 'three': set([3]), 'two': set([2]), 'one': set([1])}
        """
        # passing self with *args ensures that we can use
        # self as keyword for initializing a DictSet
        # Example: DictSet(self='abc', other='efg')
    
        if len(args)==1:
            args[0].update({}, **kwds)
            
        elif len(args)==2:
            args[0].update(args[1], **kwds)

        elif len(args) > 2 : raise \
            TypeError('DictSet expected at most 1 arguments, got %d'%(len(args)-1))
        
    def update(*args, **kwds): # args[0] -> 'self'
        """
        update(...)
            Update a DictSet with the union of itself and others.

            a|=b  <==> a.update(b)
            
          Example:        
            >>> L=DictSet({'a':[1,2,3],'b':[2,3]})
            >>> M=DictSet({'b':[1,2,3],'c':[2,3,4]})
            >>> L.update(M)

          The calling DictSet is modified:
            >>> L
            {'a': set([1, 2, 3]), 'c': set([2, 3, 4]), 'b': set([1, 2, 3])}
            >>> M
            {'c': set([2, 3, 4]), 'b': set([1, 2, 3])}

          When d is empty nothing is updated:
            >>> M=DictSet({'b':[1,2,3],'c':[2,3,4]})
            >>> M.update({})
            >>> M
            {'c': set([2, 3, 4]), 'b': set([1, 2, 3])}
            
        """
##        print 'update',args
        # check the length of args
        if len(args) > 2 : raise \
            TypeError('DictSet expected at most 1 arguments, got %d'%(len(args)-1))

        # Make sure args can be mapped to a DictSet before
        # we start adding them.
        elif len(args)==2:
            obj=args[1]

            # if obj is a DictType we can avoid checking
            # to make sure it is hashable an iterable
            if type(obj)==DictSet:
                pass
            
            # Check using duck typing
            elif hasattr(obj, '__getitem__'):

                # obj is dict or dict subclass
                if hasattr(obj, 'keys'):
                    for k,val in obj.items():
                        try    : k.__hash__()
                        except : raise \
                    TypeError("unhashable type: '%s'"%type(k).__name__)

                        try    : val.__iter__()
                        except :
                            if type(val)!=str : raise \
                    TypeError("'%s' object is not iterable"%type(val).__name__)

                # obj is list/tuple or list/tuple subclass
                else:
                    for item in obj:
                        try    : (k,val)=item
                        except : raise \
                    TypeError('could not unpack arg to key/value pairs')

                        try    : k.__hash__()
                        except : raise \
                    TypeError("unhashable type: '%s'"%type(k).__name__)

                        try    : val.__iter__()
                        except :
                            if type(val)!=str : raise \
                    TypeError("'%s' object is not iterable"%type(val).__name__)

            # obj is not iterable, e.g. an int, float, etc.
            else:
                raise TypeError("'%s' object is not iterable"%type(obj).__name__)
                    
        # check the keyword arguments
        for (k,val) in kwds.items():
            # unhashable keyword argumnents don't make it to the point 
            # so we just need to check that the values are iterable
            try    : val.__iter__()
            except :
                if type(val)!=str: raise \
                    TypeError("'%s' object is not iterable"%type(val).__name__)


        # At this point we can be fairly certain the args and kwds 
        # will successfully initialize. Now we can go back through
        # args and kwds and add them to ds
        if len(args)==2:
            obj=args[1]

            # Check using duck typing
            if hasattr(obj, '__getitem__'):

                # obj is dict or dict subclass
                if hasattr(obj, 'keys'):
                    for k,val in obj.items():
                        if not k in args[0].keys():
                            args[0][k]=set(val)
                        args[0][k]|=set(val)


                # obj is list/tuple or list/tuple subclass
                else:
                    for item in obj:
                        (k,val)=item
                        if not k in args[0].keys():
                            args[0][k]=set(val)
                        args[0][k]|=set(val)

        # Now add keyword arguments
        for (k,val) in kwds.items():
            if not k in args[0].keys():
                args[0][k]=set(val)
            args[0][k]|=set(val)

    def __ior__(self, d): # overloads |=
        """
        update(...)
            Update a DictSet with the union of itself and others.

            a|=b  <==> a(b)

          Example:        
            >>> L=DictSet({'a':[1,2,3],'b':[2,3]})
            >>> M=DictSet({'b':[1,2,3],'c':[2,3,4]})
            >>> L|=M
            
          The calling DictSet is modified:
            >>> L
            {'a': set([1, 2, 3]), 'c': set([2, 3, 4]), 'b': set([1, 2, 3])}
            >>> M
            {'c': set([2, 3, 4]), 'b': set([1, 2, 3])}

          When d is empty nothing is updated:
            >>> M=DictSet({'b':[1,2,3],'c':[2,3,4]})
            >>> M|={}
            >>> M
            {'c': set([2, 3, 4]), 'b': set([1, 2, 3])}
        """        
        if type(d)!=DictSet:
            try    : d=DictSet(copy(d))
            except : raise
        
        return self.union(d)
    
    def __eq__(self,d): # overloads ==
        """
        __eq__(...)
            Reports whether another DictSet is equal to this
            DictSet. Comparisons with non-DictSet type are
            valid and return False.

            a==b  <==>  a.__eq__(b)

          Examples:
            >>> L=DictSet({'a':[1,2,3],'b':[1,2,3,4]})
            >>> L==[(5.,4),(5.,4)]
            False

             >>> M={'a':[1,3,2],'b':[2,3,4,4,4,1],'c':[3]}
            >>> L==M
            False
            
            >>> M={'a':[1,3,2],'b':[2,3,4,4,4,1],'c':[]}
            >>> L==M
            True

        """
##        print self,d
        
        # Fails of d is not mappable with iterable values
        try    : d=DictSet(d)
        except : return False

        # check to see if self and d have the same keys
        # if they don't we know they aren't equal and
        # can return False
        if len(set((k for (k,v) in self.items() if len(v)!=0))  ^ \
               set((k for (k,v) in d.items()    if len(v)!=0))) > 0:
            return False

        # at this point we know they have the same keys
        # if all the non-empty set differences have 0 cardinality
        # the sets are equal
        return sum([len(self.get(k,[])^d.get(k,[])) for k in self])==0

    def __ne__(self,d): # overloads !=
        """
        __ne__(...)
            Reports whether another DictSet is not equal to
            this DictSet. Comparisons with non-DictSet type
            are valid and return True.

            a==b  <==>  a.__ne__(b)

          Examples:
            >>> L=DictSet({'a':[1,2,3],'b':[1,2,3,4]})
            >>> L!=[(5.,4),(5.,4)]
            True
            
            >>> M={'a':[1,2,3],'b':[1,2,3,4,4,4]}
            >>> L!=M
            False

            >>> M={'a':[1,2,3],'b':[1,2,3,4,4,4,5]}
            >>> L!=M
            True
        """
        # Fails of d is not mappable with iterable values
        try    : d=DictSet(d)
        except : return True

        # check to see if self and d have the same keys
        # if they don't we know they aren't equal and
        # can return False
        if len(set((k for (k,v) in self.items() if len(v)!=0))  ^ \
               set((k for (k,v) in d.items()    if len(v)!=0))) > 0:
            return True

        # at this point we know they have the same keys
        # if all the set differences have 0 cardinality
        # the sets are equal
        return sum((len(self.get(k,[])^d.get(k,[])) for k in self))!=0
        
    def issubset(self, d):
        """
        issubset(...)
            Report whether another set contains this DictSet.

            a<=b  <==> a.issubset(b)
            
        Examples:
            >>> L=DictSet({'a':[1,2,3],'b':[2,3]})
            >>> M=DictSet({'a':[1,2,3],'b':[2,3,4]})
            >>> L.issubset(M)
            True
            >>> M.issubset(L)
            False
            >>> L.issubset(L)
            True
            >>> L.issubset({})
            False

          Ignores empty sets:  
            >>> L=DictSet({'a':[1,2,3],'b':[2,3],'c':[]})
            >>> L.issubset(M)
            True
        """
        if type(d)!=DictSet:
            try    : d=DictSet(copy(d))
            except : raise
            
        if self==d=={}: return True
            
        return all((self.get(k,[])<=d.get(k,[]) for k in set(self)|set(d)))

    def __le__(self,d): # overloads <=
        """
        issubset(...)
            Report whether another DictSet contains this DictSet.

            a<=b  <==> a.issubset(b)
            
        Examples:
            >>> L=DictSet({'a':[1,2,3],'b':[2,3]})
            >>> M=DictSet({'a':[1,2,3],'b':[2,3,4]})
            >>> L<=M
            True
            >>> M<=L
            False
            >>> L<=L
            True
            >>> L<={}
            False
        """        
        if type(d)!=DictSet:
            try    : d=DictSet(copy(d))
            except : raise
        
        return self.issubset(d)

    def issuperset(self, d):
        """
        issuperset(...)
            Report whether this DictSet contains another DictSet.

            a>=b  <==> a.issuperset(b)
            
        Examples:
            >>> L=DictSet({'a':[1,2,3],'b':[2,3]})
            >>> M=DictSet({'a':[1,2,3],'b':[2,3,4]})
            >>> M.issuperset(L)
            True
            >>> L.issuperset(M)
            False
            >>> L.issuperset(L)
            True
            >>> L.issuperset({})
            True
        """        
        if type(d)!=DictSet:
            try    : d=DictSet(copy(d))
            except : raise

        if self==d=={}: return True
            
        return all((self.get(k,[])>=d.get(k,[]) for k in set(self)|set(d)))

    def __ge__(self,d): # overloads >=
        """
        issuperset(...)
            Report whether this DictSet contains another DictSet.

            a>=b  <==> a.issuperset(b)
            
        Examples:
            >>> L=DictSet({'a':[1,2,3],'b':[2,3]})
            >>> M=DictSet({'a':[1,2,3],'b':[2,3,4]})
            >>> M>=L
            True
            >>> L>=M
            False
            >>> L>=L
            True
            >>> L>=DictSet()
            True
        """        
        if type(d)!=DictSet:
            try    : d=DictSet(copy(d))
            except : raise
        
        return self.issuperset(d)
        
    def union(self, d):
        """
        union(...)
            Return the union of DictSets as a new DictSet.
            
            (i.e. all elements that are in either sets of
             the DictSets.)

            a|b  <==> a.union(b)
            
          Example:        
            >>> L=DictSet({'a':[1,2,3],'b':[2,3]})
            >>> M=DictSet({'b':[1,2,3],'c':[2,3,4]})
            >>> L.union(M)
            {'a': set([1, 2, 3]), 'c': set([2, 3, 4]), 'b': set([1, 2, 3])}
            >>> L.union(M) == M.union(L)
            True
            >>> L.union({})==L
            True
            
          The original DictSets stay intact:
            >>> L
            {'a': set([1, 2, 3]), 'b': set([2, 3])}
            >>> M
            {'c': set([2, 3, 4]), 'b': set([1, 2, 3])}
        """        
        if type(d)!=DictSet:
            try    : d=DictSet(copy(d))
            except : raise

        foo=deepcopy(self)
        for k in set(foo)|set(d):
            foo.setdefault(k,[])\
               .update(d.get(k,[]))
            if len(foo[k])==0:
                del foo[k]

        return foo

    def __or__(self,d): # overloads |
        """
        union(...)
            Return the union of DictSets as a new DictSet.
            
            (i.e. all elements that are in either sets of
             the DictSets.)

            a|b  <==> a.union(b)
            
          Example:
            >>> L=DictSet({'a':[1,2,3],'b':[2,3]})
            >>> M=DictSet({'b':[1,2,3],'c':[2,3,4]})
            >>> L|M
            {'a': set([1, 2, 3]), 'c': set([2, 3, 4]), 'b': set([1, 2, 3])}
            >>> L|M == M|L
            True
            >>> L|{}==L
            True
            
          The original DictSets stay intact:
            >>> L
            {'a': set([1, 2, 3]), 'b': set([2, 3])}
            >>> M
            {'c': set([2, 3, 4]), 'b': set([1, 2, 3])}
        """        
        if type(d)!=DictSet:
            try    : d=DictSet(copy(d))
            except : raise
        
        return self.union(d)

    def intersection(self, d):
        """
        intersection(...)
            Return the intersection of two or more DictSets as a
            new DictSet.
            
            (i.e. elements that are common to all of the sets of
             the DictSets.)

            a&b  <==> a.intersection(b)
            
          Example:
            >>> L=DictSet({'a':[1,2,3],'b':[5,6,7]})
            >>> M=DictSet({'a':[2,3,4],'b':[4,5,6,7],'c':[4,5,6]})
            >>> L.intersection(M)
            {'a': set([2, 3]), 'b': set([5, 6, 7])}
            >>> M.intersection({})
            {}

          The original DictSets stay intact:
            >>> L
            {'a': set([1, 2, 3]), 'b': set([5, 6, 7])}
            >>> M
            {'a': set([2, 3, 4]), 'c': set([4, 5, 6]), 'b': set([4, 5, 6, 7])}
        """        
        if type(d)!=DictSet:
            try    : d=DictSet(copy(d))
            except : raise

        # handle case where d=={}
        if d=={}: return {}
        
        foo=deepcopy(self)
        for k in set(foo)|set(d):
            foo.setdefault(k,[])\
               .intersection_update(d.get(k,[]))
            if len(foo[k])==0:
                del foo[k]

        return foo

    def __and__(self, d): # overloads &
        """
        intersection(...)
            Return the intersection of two or more DictSets as a
            new DictSet.
            
            (i.e. elements that are common to all of the sets of
             the DictSets.)

            a&b  <==> a.intersection(b)
            
          Example:
            >>> L=DictSet({'a':[1,2,3],'b':[5,6,7]})
            >>> M=DictSet({'a':[2,3,4],'b':[4,5,6,7],'c':[4,5,6]})
            >>> L&M
            {'a': set([2, 3]), 'b': set([5, 6, 7])}
            >>> L&{}
            {}

          The original DictSets stay intact:
            >>> L
            {'a': set([1, 2, 3]), 'b': set([5, 6, 7])}
            >>> M
            {'a': set([2, 3, 4]), 'c': set([4, 5, 6]), 'b': set([4, 5, 6, 7])}
        """        
        if type(d)!=DictSet:
            try    : d=DictSet(copy(d))
            except : raise
        
        return self.intersection(d)

    def difference(self, d):
        """
        difference(...)
            Return the difference of two or more DictSets as a
            new DictSet.
            
            (i.e. all elements that are in the sets of one dict
             but not the others.)
        
            a-b  <==> a.difference(b)
            
          Example:
            >>> L=DictSet({'a':[1,2,3],'b':[5,6,7]})
            >>> M=DictSet({'a':[2,3,4],'b':[4,5,6,7],'c':[4,5,6]})
            >>> L.difference(M)
            {'a': set([1])}
            >>> L.difference(M)==M.difference(L)
            False
            >>> L.difference({})==L
            True
            
          The original DictSets stay intact:
            >>> L
            {'a': set([1, 2, 3]), 'b': set([5, 6, 7])}
            >>> M
            {'a': set([2, 3, 4]), 'c': set([4, 5, 6]), 'b': set([4, 5, 6, 7])}
        """        
        if type(d)!=DictSet:
            try    : d=DictSet(copy(d))
            except : raise

        foo=deepcopy(self)
        for k in set(foo)|set(d):
            foo.setdefault(k,[])\
               .difference_update(d.get(k,[]))
            if len(foo[k])==0:
                del foo[k]

        return foo

    def __sub__(self, d): # overloads -
        """
        difference(...)
            Return the difference of two or more DictSets as a
            new DictSet.
            
            (i.e. all elements that are in the sets of this
             DictSet but not the others.)

            a-b  <==> a.difference(b)
        
          Example:
            >>> L=DictSet({'a':[1,2,3],'b':[6,7,8]})
            >>> M=DictSet({'a':[2,3,4],'b':[4,5,6,7],'c':[4,5,6]})
            >>> L-M
            {'a': set([1]), 'b': set([8])}
            >>> L - {}==L
            True
            
          The original DictSets stay intact:
            >>> L
            {'a': set([1, 2, 3]), 'b': set([6, 7, 8])}
            >>> M
            {'a': set([2, 3, 4]), 'c': set([4, 5, 6]), 'b': set([4, 5, 6, 7])}
        """        
        if type(d)!=DictSet:
            try    : d=DictSet(copy(d))
            except : raise
        
        return self.difference(d)

    def symmetric_difference(self, d):
        """
        symmetric_difference(...)
            Return the symmetric difference of two DictSets as a
            new DictSet.
            
            (i.e. all elements that are in exactly one of the
             sets of the DictSets.)

            a^b  <==> a.symmetric_difference(b)

          Examples:
            >>> L=DictSet({'a':[1,2,3],'b':[5,6,7]})
            >>> M=DictSet({'a':[2,3,4],'b':[4,5,6,7],'c':[4,5,6]})
            >>> L.symmetric_difference(M)
            {'a': set([1, 4]), 'c': set([4, 5, 6]), 'b': set([4])}
            >>> L.symmetric_difference(M) == M.symmetric_difference(L)
            True
            >>> L.symmetric_difference(L)
            {}
            >>> L.symmetric_difference({})==L
            True
            
        """        
        if type(d)!=DictSet:
            try    : d=DictSet(copy(d))
            except : raise

        foo=deepcopy(self)
        for k in set(foo)|set(d):
            foo.setdefault(k,[])\
               .symmetric_difference_update(d.get(k,[]))
            if len(foo[k])==0:
                del foo[k]

        return foo

    def __xor__(self, d): # overloads ^
        """
        symmetric_difference(...)
            Return the symmetric difference of two DictSets as a
            new DictSet.
            
            (i.e. for each DictSet all elements that are in
             exactly one of the sets .)

            a^b  <==> a.symmetric_difference(b)

          Examples:
            >>> L=DictSet({'a':[1,2,3],'b':[5,6,7]})
            >>> M=DictSet({'a':[2,3,4],'b':[4,5,6,7],'c':[4,5,6]})
            >>> L^M
            {'a': set([1, 4]), 'c': set([4, 5, 6]), 'b': set([4])}
            >>> L^M == M^L
            True
            >>> L^L
            {}
            >>> L^{}==L
            True
        """        
        if type(d)!=DictSet:
            try    : d=DictSet(copy(d))
            except : raise
        
        return self.symmetric_difference(d)

    def intersection_update(self, d):
        """
        intersection_update(...)
            Update a DictSet with the intersection of
            itself and another.

            a&=b  <==> a.intersection_update(b)
            
          Example:        
            >>> L=DictSet({'a':[1,2,3],'b':[2,3]})
            >>> M=DictSet({'b':[1,2,3],'c':[2,3,4]})
            >>> L.intersection_update(M)
            
          The calling DictSet is modified:
            >>> L
            {'b': set([2, 3])}
            >>> M
            {'c': set([2, 3, 4]), 'b': set([1, 2, 3])}
 
          When d is self is cleared:
            >>> M=DictSet({'b':[1,2,3],'c':[2,3,4]})
            >>> M.intersection_update({'c':[2]})
            >>> M
            {'c': set([2])}
        """        
        if type(d)!=DictSet:
            try    : d=DictSet(copy(d))
            except : raise
        
        for k in set(self)|set(d):
            self.setdefault(k,[])\
                .intersection_update(d.get(k,[]))
            if len(self[k])==0:
                del self[k]


    def __iand__(self, d): # overloads &=
        """
        intersection_update(...)
            Update a DictSet with the intersection of
            itself and another.

            a&=b  <==> a.intersection_update(b)
            
          Example:        
            >>> L=DictSet({'a':[1,2,3],'b':[2,3]})
            >>> M=DictSet({'b':[1,2,3],'c':[2,3,4]})
            >>> L&=M
            
          The calling DictSet is modified:
            >>> L
            {'b': set([2, 3])}
            >>> M
            {'c': set([2, 3, 4]), 'b': set([1, 2, 3])}

          When d is empty nothing is updated:
            >>> M=DictSet({'b':[1,2,3],'c':[2,3,4]})
            >>> M&={}
            >>> M
            {}

          Should remove empty sets
            >>> L=DictSet({'a':[1,2,3],'b':[2,3],'c':[]})
            >>> M=DictSet({'a':[1,2,3],'b':[2,3,4]})
            >>> L&=M # intersection update
            >>> L
            {'a': set([1, 2, 3]), 'b': set([2, 3])}
        """        
        if type(d)!=DictSet:
            try    : d=DictSet(copy(d))
            except : raise
        
        return self.intersection(d)
        
    def difference_update(self, d):
        """
        difference_update(...)
            Remove all elements of another DictSet from this DictSet.

            a-=b  <==> a.difference_update(b)
            
          Example:
            >>> L=DictSet({'a':[1,2,3],'b':[6,7,8]})
            >>> M=DictSet({'a':[2,3,4],'b':[4,5,6,7],'c':[4,5,6]})
            >>> L.difference_update(M)
        
          The calling DictSet is modified:
            >>> L
            {'a': set([1]), 'b': set([8])}
            >>> M
            {'a': set([2, 3, 4]), 'c': set([4, 5, 6]), 'b': set([4, 5, 6, 7])}

          When d is empty self is cleared:
            >>> M=DictSet({'b':[1,2,3],'c':[2,3,4]})
            >>> M.difference_update({})
            >>> M
            {'c': set([2, 3, 4]), 'b': set([1, 2, 3])}
        """        
        if type(d)!=DictSet:
            try    : d=DictSet(copy(d))
            except : raise
        
        for k in set(self)|set(d):
            self.setdefault(k,[])\
                .difference_update(d.get(k,[]))
            if len(self[k])==0:
                del self[k]

    def __isub__(self, d): # overloads -=
        """
        difference_update(...)
            Remove all elements of another DictSet from this DictSet.

            a-=b  <==> a.difference_update(b)
            
          Example:
            >>> L=DictSet({'a':[1,2,3],'b':[6,7,8]})
            >>> M=DictSet({'a':[2,3,4],'b':[4,5,6,7],'c':[4,5,6]})
            >>> L-=M
        
          The calling DictSet is modified:
            >>> L
            {'a': set([1]), 'b': set([8])}
            >>> M
            {'a': set([2, 3, 4]), 'c': set([4, 5, 6]), 'b': set([4, 5, 6, 7])}
            
          When d is empty nothing is updated:
            >>> M=DictSet({'b':[1,2,3],'c':[2,3,4]})
            >>> M-={}
            >>> M
            {'c': set([2, 3, 4]), 'b': set([1, 2, 3])}
        """        
        if type(d)!=DictSet:
            try    : d=DictSet(copy(d))
            except : raise
        
        return self.difference(d)
        
    def symmetric_difference_update(self, d):
        """
        symmetric_difference_update(...)
            Update a DictSet with the symmetric difference of
            itself and another.

            a^=b  <==> a.symmetric_difference_update(b)
            
          Example:
            >>> L=DictSet({'a':[1,2,3],'b':[5,6,7]})
            >>> M=DictSet({'a':[2,3,4],'b':[4,5,6,7],'c':[4,5,6]})
            >>> L.symmetric_difference_update(M)
        
          The calling DictSet is modified:
            >>> L
            {'a': set([1, 4]), 'c': set([4, 5, 6]), 'b': set([4])}
            >>> M
            {'a': set([2, 3, 4]), 'c': set([4, 5, 6]), 'b': set([4, 5, 6, 7])}
            
          When d is empty nothing is updated:
            >>> M=DictSet({'b':[1,2,3],'c':[2,3,4]})
            >>> M.symmetric_difference_update({})
            >>> M
            {'c': set([2, 3, 4]), 'b': set([1, 2, 3])}
        """        
        if type(d)!=DictSet:
            try    : d=DictSet(copy(d))
            except : raise
        
        for k in set(self)|set(d):
            self.setdefault(k,[])\
                .symmetric_difference_update(d.get(k,[]))
            if len(self[k])==0:
                del self[k]

    def __ixor__(self, d): # overloads ^=
        """
        symmetric_difference_update(...)
            Update a DictSet with the symmetric difference of
            itself and another.

            a^=b  <==> a.symmetric_difference_update(b)

          Example:
            >>> L=DictSet({'a':[1,2,3],'b':[5,6,7]})
            >>> M=DictSet({'a':[2,3,4],'b':[4,5,6,7],'c':[4,5,6]})
            >>> L.symmetric_difference_update(M)
        
          The calling DictSet is modified:
            >>> L
            {'a': set([1, 4]), 'c': set([4, 5, 6]), 'b': set([4])}
            >>> M
            {'a': set([2, 3, 4]), 'c': set([4, 5, 6]), 'b': set([4, 5, 6, 7])}
            
          When d is empty nothing is updated:
            >>> M=DictSet({'b':[1,2,3],'c':[2,3,4]})
            >>> M^={}
            >>> M
            {'c': set([2, 3, 4]), 'b': set([1, 2, 3])}
        """        
        if type(d)!=DictSet:
            try    : d=DictSet(copy(d))
            except : raise
        
        return self.symmetric_difference(d)

    def add(self, k, v):
        """
        add(...)
            Add an element to a DictSet with key given by k.
            
            This has no effect if the element is already present.

          Handling sets of numbers:
            >>> L=DictSet({'a':[1,2,3,4],'b':[5,6,7]})
            >>> L.add('b',8)
            >>> L
            {'a': set([1, 2, 3, 4]), 'b': set([5, 6, 7, 8])}
            >>> L.add('c',10)
            >>> L
            {'a': set([1, 2, 3, 4]), 'c': set([10]), 'b': set([5, 6, 7, 8])}
            >>> L.add('c',10)
            >>> L
            {'a': set([1, 2, 3, 4]), 'c': set([10]), 'b': set([5, 6, 7, 8])}
            
          Handling sets of letters:
            >>> A=DictSet({1:'abcd',2:'efg'})
            >>> A.add(2,'h')
            >>> A
            {1: set(['a', 'c', 'b', 'd']), 2: set(['e', 'g', 'f', 'h'])}
            >>> A.add(3,'hello')
            >>> A[3]
            set(['hello'])
        """
        try    : k.__hash__()
        except : raise TypeError("unhashable type: '%s'"%type(k).__name__)

        
        if k not in self:
            self[k]=set()

        # it is much faster to call the sets add method directly
        # then to go through self.update
        self[k].add(v)

    def __setitem__(self,k,val):
        """
          Handling sets of numbers:
            >>> L=DictSet()
            >>> L['a']=[1,2,3,4]
            >>> L
            {'a': set([1, 2, 3, 4])}

          Handling sets of letters:
            >>> A=DictSet()
            >>> A[1]='xyz'
            >>> A
            {1: set(['y', 'x', 'z'])}

          Handling sets of words:
            >>> C=DictSet({1:['abc','bcd','def']})
            >>> C
            {1: set(['abc', 'bcd', 'def'])}
            >>> C[2]=['qrs','efg','xyz']
            >>> C
            {1: set(['abc', 'bcd', 'def']), 2: set(['xyz', 'qrs', 'efg'])}
        """
        try    : k.__hash__()
        except : raise TypeError("unhashable type: '%s'"%type(k).__name__)

        try    : val.__iter__()
        except :
            if type(val)==str : val=[c for c in val]
            else : raise \
                 TypeError("'%s' object is not iterable"%type(val).__name__)
        
        if type(val)==set : dict.__setitem__(self, k, val)
        else              : dict.__setitem__(self, k, set(val))

    def __contains__(self, k):
        """

          Examples:
            >>> L=DictSet({'a':[],'b':[1,2,3],'c':[1]})
            >>> 'a' in L
            False
            >>> 'b' in L
            True
            >>> 'c' in L
            True
        """
        try    : k.__hash__()
        except : raise TypeError("unhashable type: '%s'"%type(k).__name__)

        return k in [key for (key,val) in self.items() if len(val)>0]

    def get(self, k, val=None):
        """
        setdefault(...)
            returns set at self[k] if k is in self,
            if k is not in self it returns val as
            a set.

          Example:
            >>> L=DictSet({'a':[1,2,3,4]})
            >>> L.get('a')
            set([1, 2, 3, 4])

            >>> L.get('b')
            
            >>> L.get('b',[])
            set([])

            >>> L.get('b',[5,6,7,8])
            set([8, 5, 6, 7])
        """
        try    : k.__hash__()
        except : raise TypeError("unhashable type: '%s'"%type(k).__name__)

        if k in self  : return self[k]
        elif val==None : return

        try    : val.__iter__()
        except :
            if type(val)==str : val=[c for c in val]
            else : raise \
                 TypeError("'%s' object is not iterable"%type(val).__name__)
        
        return set(val)

    def setdefault(self, k, val=None):
        """
        setdefault(...)
            setdefault() is like get(), except that if k is missing,
            val is both returned and inserted into the dictionary as
            the value of k. val defaults to None.

          Example:
            >>> L=DictSet({'a':[1,2,3,4]})
            >>> L.setdefault('a')
            set([1, 2, 3, 4])

            >>> b=L.setdefault('b')

            >>> L.setdefault('b',[5,6,7,8])
            set([8, 5, 6, 7])

            >>> L
            {'a': set([1, 2, 3, 4]), 'b': set([8, 5, 6, 7])}

            >>> L.setdefault('c',[])
            set([])

            >>> L
            {'a': set([1, 2, 3, 4]), 'c': set([]), 'b': set([8, 5, 6, 7])}
            
        """
        try    : k.__hash__()
        except : raise TypeError("unhashable type: '%s'"%type(k).__name__)

        if k in self  : return self[k]
        elif val==None : return

        try    : val.__iter__()
        except :
            if type(val)==str : val=[c for c in val]
            else : raise \
                 TypeError("'%s' object is not iterable"%type(val).__name__)

        if val!=None:
            dict.__setitem__(self, k, set(val))
            return self[k]
        else:
            return set([])
        
        
    def copy(self):
        """
        copy(...)
            Return a shallow copy of a DictSet.

          Examples:
            >>> L=DictSet({'a':[1,2,3],'b':[2,3]})
            >>> M=L.copy()
            >>> M.add('c',4)
            >>> L
            {'a': set([1, 2, 3]), 'b': set([2, 3])}
            >>> M
            {'a': set([1, 2, 3]), 'c': set([4]), 'b': set([2, 3])}
        """
        return copy(self)
    
    def remove(self, k, v):
        """
        remove(...)
            Remove an element from a DictSet with key given by k;

            DictSet must contain key k.
            If k is not a key, raise a KeyError.
            
            v must be a member of set self[k].
            If the element is not a member, raise a KeyError.

            see also: DictSet.discard
            
          Examples:
            >>> L=DictSet({'a':[1,2,3],'b':[2,3]})
            >>> L.remove('a',3)
            >>> L
            {'a': set([1, 2]), 'b': set([2, 3])}
        """
        try    : k.__hash__()
        except : raise TypeError("unhashable type: '%s'"%type(k).__name__)

        if k not in self:
            raise KeyError(k)
        
        try    : self[k].remove(v)
        except : raise
            
    def discard(self, k, v):
        """
        discard(...)
            Remove an element from a DictSet if it is a member.

            If DictSet does not have k as a key, do nothing.
            If the v is not a member of self[k], do nothing.

            see also: DictSet.remove

          Examples:
            >>> L=DictSet({'a':[1,2,3],'b':[2,3]})
            >>> L.discard('a',3)
            >>> L
            {'a': set([1, 2]), 'b': set([2, 3])}
            >>> L.discard('c',4)
            >>> L.discard('a',4)
        """
        try    : k.__hash__()
        except : raise TypeError("unhashable type: '%s'"%type(k).__name__)

        if k in self:
            self[k].discard(v)

if __name__ == "__main__":
    import doctest
##    doctest.testmod()
    doctest.testmod(verbose=True,report=True)



