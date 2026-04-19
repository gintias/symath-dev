# Project Context

This is a Python library supporting graduate-level math self-study. The goal is to
implement abstract structures (sets, set operations, posets, lattices, finitely presented categories,
universal algebras, well-founded relations) to complement reading in:

- Enderton, *Elements of Set Theory*
- Bergman, *An Invitation to General Algebra and Universal Constructions*
- Awodey, *Category Theory*

## Coding context

- I am rebuilding Python fluency after a long gap. Previous experience: basic data
  structures (BSTs, queues, hash tables) from an undergrad CS course.
- I want to write code myself and ask for review, not have code generated for me.
- Prefer idiomatic modern Python with type hints. Explain Python-specific idioms
  when you use them; I know the math, not the language.
- All structures are finite unless explicitly noted. Don't suggest lazy/infinite
  representations without discussion.

## Mathematical context

- Use LaTeX freely in explanations (`$...$` for inline).
- Align terminology with the books above when relevant.
- Flag when a Python construct has a meaningful mathematical analog (e.g.
  `frozenset` as a carrier, `__eq__`/`__hash__` and quotient structures).