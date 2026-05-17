from copy import deepcopy  
import inspect

class Set:

###PRIMITIVE SET BEHAVIOUR

    def __init__(self, *elements):

        temp = []        
        for i in elements:
            if i not in temp:
                temp.append(i)
        self._values = list(temp)
        return
    
    def __iter__(self):
        return iter(self._values)

    def __bool__(self):
        return not self.is_empty()

    def __contains__(self, element):
        return self._linear_search(element) != -1

    def __len__(self):
        return len(self._values)
    
    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        if len(self) != len(other):
            return False
        for element in self._values:
            if element not in other._values:
                return False
        return True
            
    def _linear_search(self, key):

        found = False
        i = 0
        while not found and i<len(self._values):
            if self._values[i]==key:
                found = True
            else:
                i+=1
        if not found:
            i=-1

        return i

    def __str__(self):
        if not self._values:
            return "∅"
        return "{" + ", ".join(str(x) for x in self._values) + "}"

###SET OPERATIONS
    def union(self, other = None):
        if other is None:
            s = Set()
            for mem in self:
                for el in mem:
                    s = s._add_elements(el)    
            return s
        if not isinstance(other, type(self)):
            return NotImplemented
        
        return Set(*self._values, *other._values)

    def intersection(self, other=None):

        if other is None:
            it = iter(self)
            result = next(it)

            for member in it:
                result = result.intersection(member)

            return result

        
        if not isinstance(other, type(self)):
                return NotImplemented
        
        vals = []
        for m in self:
            if m in other:
                vals.append(m)

        return Set(*vals)

    def complement(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        new_set = Set()
        for element in self.union(other):
            if element in self and element not in other:
                new_set._add(element)
        return new_set

    def power_set(self):
        members = self.get_members()
        subsets = []

        for size in range(0, len(members) + 1):
            for indexes in combinations(len(members), size):
                subset_members = [members[index] for index in indexes]
                subsets.append(Set(*subset_members))

        return Set(*subsets)
    
    def pair_set(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return Set(self, other)

    def product(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        
        s = [OrderedPair(a,b) for a in self for b in other]
        return Set(*s)

    def singleton(self):
        return Set(self)
    
        return Set(val)

    def adjPoin(self, other):
        return Set.union(self, Set(other))

    def _add_elements(self, *elements):
         
        vals = self.get_members()
        for element in elements:
            if element not in vals:
                vals.append(element)

        return Set(*vals)

    def _remove_elements(self, *elements):
        
        vals = self.get_members()
        
        for element in elements:
            if element in self:
                vals.remove(element)
        
        return Set(*vals)

    def get_members(self):
        return deepcopy(self._values)
    





class OrderedPair:
    def __init__(self, a, b):
        self._first = a
        self._second = b
        self._kuratowski = Set(Set(a), Set(a, b))

    @property
    def first(self):
        return self._first

    @property
    def second(self):
        return self._second
###PREDICATES / TESTABLES

    def is_subset(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented

        return self == self.intersection(other)
    
    def is_proper_subset(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.is_subset and self != other

    def is_empty(self):
        return len(self._values) == 0    

    def is_ordered_pair(self):
        elements = self.get_members()
        if len(self) == 1 and Set(self.get_members()[0][0]) == self:
            return True
        if len(elements) == 2 and isinstance(elements[0], type(self)) and isinstance(elements[1], type(self)) and len(elements[0]) == 1 and len(elements[1]) == 2 and elements[1].get_members()[0]==elements[0]:
            return True
    
        return False
    def as_set(self):
        return self._kuratowski

    def __eq__(self, other):
        if not isinstance(other, OrderedPair):
            return NotImplemented
        return self._first == other._first and self._second == other._second

    def __str__(self):
        return f"⟨{self._first}, {self._second}⟩"






    
    def has_cardinality(self, n):
        return len(self) == n


def combinations(N, n, start=0):
    if n == 0:
        return [[]]
    result = []
    for first in range(start, N - n + 1):
        for rest in combinations(N, n - 1, first + 1):
            result.append([first] + rest)
    return result

Rule:          name, arity, apply