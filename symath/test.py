from symath.SetTheory import Set, OrderedPair

S = Set("A","B","C","D")
L = Set("C","D")
T= Set(Set(Set.singleton("x"), Set.pair_set("x","y")), Set.pair_set("z","y"))
P = Set(Set.singleton("x"), Set.pair_set("x","y"))

print(T.intersection())
print(T.union())
print(Set.union(T))
print(Set.union(T, T))

print(P.intersection().union())



def combinations(N, n, start=0):
    if n == 0:
        return [[]]
    result = []
    for first in range(start, N - n + 1):
        for rest in combinations(N, n - 1, first + 1):
            result.append([first] + rest)
    return result



x = Set("A")
y = Set("B")
t = Set.union(x,y).power_set().power_set()

card = lambda x: len(x)
has_card = lambda x: lambda n: card(x) == n




cond = lambda x: card(x)==2
L = tuple(map(cond, t))

new=Set()
vals = t.get_members()
for i in range(0,len(L)):
    if L[i]:
        new=new.adjoin(vals[i])



print(*new.get_members())
print()



p = OrderedPair(Set(),x)
print(p)
print(p.union())
print(p.as_set())


def combinations(N, n, start=0):
    if n == 0:
        return [[]]
    result = []
    for first in range(start, N - n + 1):
        for rest in combinations(N, n - 1, first + 1):
            result.append([first] + rest)
    return result

S = Set("A","B","C","D")



