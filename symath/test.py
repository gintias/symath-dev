from SetTheory import Set, OrderedPair

S = Set("A","B","C","D")
L = Set("C","D")
T= Set(Set(Set.singleton("x"), Set.pair_set("x","y")), Set.pair_set("z","y"))
P = Set(Set.singleton("x"), Set.pair_set("x","y"))

print(T.intersection())
print(T.union())
print(Set.union(T))
print(Set.union(T, T))

print(P.intersection().union())

print(Set(*S,*L))

s = [OrderedPair(a,b) for a in S for b in L]
S = Set(*s)
print(S)