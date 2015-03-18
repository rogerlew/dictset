## General Description ##
The basic Python container types (`dict`, `list`, `set`, and `tuple`) are extremely versatile and powerful. The collections module first implemented in Python 2.4 has shown that sub-classing these containers can yield elegant solutions to the right problem. In a similar vein this project is a dict subclass for elegantly handling collections of sets. In many aspects a `DictSet` is similiar to a `defaultdict` of `sets` except it generalizes many of the set operations to the `dict`.

**Put simply, DictSet is a dict of sets that behaves like a set.**

DictSet requires **0** non-standard dependencies and should work with Python 2.5 and up.

The project described was supported by NIH Grant Number P20 RR016454 from the INBRE Program of the National Center for Research Resources.

---

> ### Table of Contents ###
> 

---

## Behold the Power of DictSet! ##
> ### Duck type comparisons ###
```
>>> DictSet({'one':[1,2,3],'two':[3,4,5]}) == [('one',[1,2,3]),('two',[3,4,5,5,5])]
True
>>>
```

> ### Set operations apply across key, value pairs ###
```
>>> L=DictSet({'a':[1,2,3],'b':[5,6,7]})
>>> M=DictSet({'a':[2,3,4],'b':[4,5,6,7],'c':[4,5,6]})
>>> L.symmetric_difference(M)
DictSet([('a', set([1, 4])), ('c', set([4, 5, 6])), ('b', set([4]))])
```

> ### Set operations are overloaded ###
```
>>> L=DictSet({'a':[1,2,3],'b':[5,6,7]})
>>> M=DictSet({'a':[2,3,4],'b':[4,5,6,7],'c':[4,5,6]})
>>> L^M
DictSet([('a', set([1, 4])), ('c', set([4, 5, 6])), ('b', set([4]))])
>>>
>>> L.intersection(Y)==L&M
True
>>> L.difference(M)==L-M
True
>>> L.union(M)==L|M
True
>>> 
```

> ### Empty key,value sets are treated as non-existent by comparisons and set operations ###
```
>>> L=DictSet({'a':[1,2,3],'b':[2,3],'c':[]})
>>> M=DictSet({'a':[1,2,3],'b':[2,3,4]})
>>> L.issubset(M)
True
>>> 'a' in L
True
>>> 'c' in L
False
```
> ### Iterator method only yields keys to non-empty sets ###
```
>>> L=DictSet({'a':[1,2,3],'b':[2,3],'c':[],'d':[]})
>>> for k in L:
	print k
a
b
>>> for k in L.keys():
	print k
a
c
b
d
>>> 
```
> ### Generator for unique combinations of elements across sets ###
```
>>> ds=DictSet({'factor 1':['left','right'],
	        'factor 2':['I','II','III'],
	        'factor 3':['test','control']})
>>>
>>> for conditions in ds.unique_combinations():
	print conditions
['left',  'I',   'control']
['left',  'I',   'test'   ]
['left',  'II',  'control']
['left',  'II',  'test'   ]
['left',  'III', 'control']
['left',  'III', 'test'   ]
['right', 'I',   'control']
['right', 'I',   'test'   ]
['right', 'II',  'control']
['right', 'II',  'test'   ]
['right', 'III', 'control']
['right', 'III', 'test'   ]
>>>
>>> # I made the formatting look pretty
```

---

## Getting Started ##
> ### Acquiring DictSet directly from cheese shop ###
> > Dictset is in the cheese shop (pypi) under "dictset." If you have setuptools all you need to do is:
```
    easy_install dictset
```
> > and you are done.

> _Assuming easy\_install is in your path. If you are not familiar with easy\_install it should be in the Scripts folder of your installation._
> > Example:
```
    C:\Python27\Scripts\easy_install.exe dictset
```

> ### Acquiring setuptools so you can acquire dictset directly from the cheeseshop ###
> > If you don't have setuptools, it is available [here](http://pypi.python.org/pypi/setuptools) (assumming you are not using Python 3).

> ### Manual installation ###
> > If you don't want to install setuptools or cannot install setuptools you can install dictset manually from the source. Just download and extract the module from http://pypi.python.org/pypi/dictset/.
> > And then run:
```
    setup.py install
```

---

## Some Basic Examples ##

> ### Importing DictSet ###
> After it is installed you simply need to import the DictSet class from the dictset module
```
from dictset import DictSet
```

> ### Initializing DictSets ###
> DictSet inherents dict and can be initialized using the same signatures available for   ordinary dictionary objects. The only difference is that the values must be iterable since they are turned into set objects.
```
>>> DictSet()
{}
>>>
>>> DictSet(one=[1],two=[2])
DictSet([('two', set([2])), ('one', set([1]))])
>>>
>>> DictSet([('one',[1]),('two',[2])])
DictSet([('two', set([2])), ('one', set([1]))])
>>>
>>> DictSet({'one':[1],'two':[2]})
DictSet([('two', set([2])), ('one', set([1]))])
>>>
```

> ### Manipulating elements with `add`, `remove`, and `discard` ###
> If you are familiar with the existing set class then you should already be familiar with `add`, `remove` and `discard`. They work the same way as they do on regular sets. The only difference is that here you have to specify a key to the set you want to manipulate.
```
>>> # adding
>>> W=DictSet({1:['BOB','FRED','JIM']})
>>> W[2]=['BILL','TOM']
>>> W.add(2,'BRIAN')
DictSet([(1, set(['BOB', 'JIM', 'FRED'])), (2, set(['BRIAN', 'BILL', 'TOM']))])
>>> 
>>> # remove an element from a specific set
>>> W.remove(2,'BRIAN')
>>> W
DictSet([(1, set(['BOB', 'JIM', 'FRED'])), (2, set(['BILL', 'TOM']))])
>>>
>>> # remove complains if key or value doesn't exist
>>> W.remove(2,'BRIAN')

Traceback (most recent call last):
    ...
KeyError: 'BRIAN'
>>>
>>> # In contrast discard will quietly return
>>> W.discard(2,'BRIAN')
>>>
```
> ### Manipulating entire sets with `add`, `remove`, and `discard` ###
> In addition to using `add`, `remove` and `discard` on specific set elements, we can also manipulate entire sets with `add`, `remove` and `discard`.
```
>>> W=DictSet()
>>>
>>> # add an empty set
>>> W.add('FRED')
>>> W
DictSet([('FRED', set([]))])
>>> W['FRED']=[1,2,3,4]
>>>
>>> # calling add again, does nothing if the key exists
>>> W.add('FRED')
>>> W
DictSet([('FRED', set([1, 2, 3, 4]))])
>>>
>>> # delete entire set with remove
>>> W.remove('FRED')
>>> W
DictSet()
>>> # remove will complain if k is not a key
>>> W.remove('FRED')
Traceback (most recent call last):
    ...
KeyError: 'FRED'
>>>
>>> # discard won't complain, even when the first argument is garbage
>>> W.discard([]) # <- that can't even be a key
>>>
```
> ### Set operations are key matched ###
```
>>> W=DictSet({1:['BOB','FRED','JIM'],2:['BILL','TOM','BRIAN']})
>>> Y=DictSet({1:['BOB','BILLY'],     2:['BILL','JOE']})
>>>
>>> # intersection
>>> W.intersection(Y) # returns a new DictSet
DictSet([(1, set(['BOB'])), (2, set(['BILL']))])
>>> 
>>> # difference
>>> W.difference(Y) # returns a new DictSet
DictSet([(1, set(['JIM', 'FRED'])), (2, set(['BRIAN', 'TOM']))])
>>>
>>> # union
>>> W.union(Y) # returns a new DictSet
DictSet([(1, set(['BILLY', 'BOB', 'JIM', 'FRED'])), (2, set(['BRIAN', 'BILL', 'JOE', 'TOM']))])
>>>
```

> ### Updating DictSets with set operations ###
```
>>> W=DictSet({1:['BOB','FRED','JIM'],2:['BILL','TOM','BRIAN']})
>>> Y=DictSet({1:['BOB','BILLY'],     2:['BILL','JOE']})
>>> 
>>> W.intersection_update(Y)
>>> W
DictSet([(1, set(['BOB'])), (2, set(['BILL']))])
>>> 
>>> # Y stays intact
DictSet([(1, set(['BILLY', 'BOB'])), (2, set(['BILL', 'JOE']))])
>>>
```
> ### Items with empty sets are discarded ###
```
>>> W=DictSet({1:['BOB','FRED','JIM'],2:['BILL','TOM','BRIAN']})
>>> Y=DictSet({1:['BOB','BILLY']})
>>> 
>>> W.intersection_update(Y)
>>> W
DictSet([(1, set(['BOB']))])
>>> 
```

> ### Items are added as necessary ###
```
>>> W=DictSet({1:['BOB','FRED','JIM']})
>>> Y=DictSet({4:['TED','GREG']})
>>>
>>> W.update(Y)
>>> W
DictSet([(1, set(['BOB', 'JIM', 'FRED'])), (4, set(['GREG', 'TED']))])
>>>
```


> ### Set comparisons ###
```
>>> # issubset and issuperset comparisons are available
>>> W=DictSet({1:'abc',2:'wxyz'})
>>> Y=DictSet({1:'abc',2:'xyz'})
>>>
>>> W.issubset(Y)
False
>>> W.issuperset(Y)
True
>>>
```

> ### Non-set comparisons ###
```
>>> # DictSet uses duck-type comparisons
>>> DictSet({'a':[1,2,4],'b':[3,4]})==[('a',[1,2,4]),('b',[3,4,4,4])]
True
>>>
>>> W=DictSet({1:'abc',2:'xyz'})
>>> Y={1:'aaaaabbbbbccccc',2:'xxxxxyyyyyzzzz'}
>>>
>>> W==Y
True
>>>
>>> # DictSets can be compared with other types
>>> W==[]
False
>>> W!=[]
True
>>>
```
> ## Using get and setdefault ##
> As with ordinary dictionaries, a `KeyError` exception is raised if argument is not in the map. The `get`(_key_, `[`_val_,`]`) and `setdefault`(_key_, `[`_val_,`]`) dict methods work mostly as you would expect.
```
>>> L=DictSet({'a':[1,2,3,4]})
>>> L['b']
Traceback (most recent call last):
    ...
KeyError: 'b'
>>> 
>>> # get when using a key in L
>>> L.get('a')
set([1, 2, 3, 4])
>>>
>>> # when using a key not in L passes quietly
>>> L.get('b')
>>>   
>>> # when key not in L the optional argument is returned as a set      
>>> L.get('b',[5,6,7,8])
set([5, 6, 7, 8])
>>>
>>> L.get('b',[])
set([])
>>>
>>> # get leaves L intact
>>> L
DictSet([('a', set([1, 2, 3, 4]))])
>>> 
```
> Now let's see what happens when we use `setdefault`(_key_, `[`_val_,`]`). It behaves similiarly to `get` except that when _val_ is not equal to `None` it will try to set the val before returning val as a set.
```
>>> L=DictSet({'a':[1,2,3,4]})
>>> 
>>> # when val is None, nothing is added to L
>>> L.setdefault('b')
>>> L
DictSet([('a', set([1, 2, 3, 4]))])
>>>
>>> # passing an empty list will add an empty set and return a pointer
>>> ptr2b=L.setdefault('b',[])
>>> ptr2b
set([])
>>> L
DictSet([('a', set([1, 2, 3, 4])), ('b', set([]))])
>>> ptr2b.update([5,6,7,8])
>>> L
DictSet([('a', set([1, 2, 3, 4])), ('b', set([5, 6, 7, 8]))])
```

> ### Caveats ###
> Keep in mind set operations remove empty sets to avoid having the memory and performance overhead of managing lots of empty sets. If your set is removed the pointer becomes unlinked to the DictSet.
```
>>> L=DictSet({'a':[1,2,3,4]})
>>> ptr2b=L.setdefault('b',[])
>>> L
DictSet([('a', set([1, 2, 3, 4])), ('b', set([]))])
>>> # setdefault has added empty set to L
>>> L&={'a':[1,2,3,4]} # intersection update
>>> L
DictSet([('a', set([1, 2, 3, 4]))])
>>> # ptr2b has been unlinked
>>> 
```

> Note that the unittest module won't work with 2.5 because it uses the_`with self.assertRaises(...)`_method.

---

## An Advanced Example ##
> Here I show how a DictSet can be used to make "where not" exclusions in tabulated data.
```
from __future__ import print_function

from random import random
from collections import OrderedDict

from dictset import DictSet, _rep_generator

# Let's build some fake tabulated data. I like to
# use dictionaries of lists where the keys
# coorspond to the column labels.
data=OrderedDict()
data['ID']   = list(range(1,17))
data['A']    = list(_rep_generator([0,1,2,3],1,4))
data['B']    = list(_rep_generator([5,6],4,2))
data['C']    = list(_rep_generator([7,8],8,1))
data['data'] = [random()*10. for i in range(16)]

# print the fake data
print('Fake Data')
print('ID\tA\tB\tC\tdata\n','='*45,sep='')
for i in range(16):
    print('\t'.join([str(data[k][i]) for k in data]))

# now we can use a dictset to exclude certain cases
# where data['A']==0 or data['A']==2 or data['C']==7
ex=DictSet({'A':[0,2],'C':[7]}) 

print('\nExcluded Data Based on ex')
print('ID\tA\tB\tC\tdata\n','='*45,sep='')
for i in range(16):

    # if the difference between the ex DictSet and the
    # conditions at the ith index is equal to the ex
    # DictSet print the row    
    if ex - [(k,[data[k][i]]) for k in data] == ex:
        print('\t'.join([str(data[k][i]) for k in data]))
```
> The output:
```
>>> ================================ RESTART ================================
>>> 
Fake Data
ID	A	B	C	data
=============================================
1	0	5	7	4.24603485738
2	0	5	8	4.56247422031
3	0	6	7	3.0493546433
4	0	6	8	0.658991184823
5	1	5	7	7.15508862079
6	1	5	8	3.86857952789
7	1	6	7	1.90367015479
8	1	6	8	8.67933435413
9	2	5	7	3.74375879417
10	2	5	8	8.97640083416
11	2	6	7	6.593210339
12	2	6	8	2.03237538715
13	3	5	7	4.51157148185
14	3	5	8	5.81649642826
15	3	6	7	3.77913770871
16	3	6	8	1.27058859878

Excluded Data Based on ex
ID	A	B	C	data
=============================================
6	1	5	8	3.86857952789
8	1	6	8	8.67933435413
14	3	5	8	5.81649642826
16	3	6	8	1.27058859878
>>> 
```

---

## An Example Using the `unique_combinations` Generator ##
> In some instances we can avoid the syntax of deeply nested loops using the unique\_combinations generator.
> Instead of doing this:
```
for A in [10,20,40,80]:
    for B in [100,800]:
        for rep in range(100):
            do_something(A,B)
```
> We can do this:
```
conditionsDict=DictSet({'A':[10,20,40,80],
                        'B':[100,800],
                      'rep':range(100)})

for A,B,rep in conditionsDict.unique_combinations():
    do_something(A,B)
```
> It is much easier to write generic code using the generator as opposed to nested loops, especially if you don't know how many arguments you are unpacking.
> ### Example ###
> Here is a rather contrived example examining the linear effects of two factors on random variables.
```
from __future__ import print_function

from random import random
from collections import Counter

from dictset import DictSet, _rep_generator

conditionsDict=DictSet({'A':[10,20,40,80],
                        'B':[100,800],
                      'rep':range(100)})

sumCounter=Counter()
for A,B,rep in conditionsDict.unique_combinations():
    sumCounter[(A,B)] += A*random() + B*random()

print('  Table of Marginal Sums')
print('='*36)
print('  A   ||   B = 100\tB = 800')
print('='*36)

for A in sorted(conditionsDict['A']):
    print('  %i  ||   '%A,end='')
    for B in sorted(conditionsDict['B']):
        print('%.3f\t'%(sumCounter[(A,B)]),end='')
    print()
```
> And the output:
```
>>> ================================ RESTART ================================
>>> 
  Table of Marginal Sums
====================================
  A   ||   B = 100	B = 800
====================================
  10  ||   5474.566	40320.148	
  20  ||   5594.594	36266.647	
  40  ||   6605.315	42428.025	
  80  ||   9066.395	41663.439	
>>> 
```