SUBSCRIPT_MAP = str.maketrans("0123456789","₀₁₂₃₄₅₆₇₈₉")
symbols = {
    "forall": "∀",
    "exists": "∃",
    "not": "¬",
    "and": "∧",
    "or": "∨",
    "implies": "→",
    "iff": "↔",
    "in": "∈",
    "union": "∪",
    "intersection": "∩",
    "subset": "⊂",
    "subseteq": "⊆",
    "empty": "∅",
}

variable = "a"
print(symbols["forall"], "x ∈ A")

to_subscript = lambda n: str(n).translate(SUBSCRIPT_MAP)


