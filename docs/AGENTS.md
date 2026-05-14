# AGENTS.md

## Project: Symath

Symath is a long-horizon symbolic mathematics and formal logic system written in Python. The project aims to build a progressively extensible framework for representing mathematical objects, symbolic constructions, logical formulas, proof structures, definitions, dependencies, and eventually large regions of formal mathematics.

This repository is still in an early foundational stage. Code quality, conceptual clarity, and architectural discipline matter more than rapid feature completion.

---

## Core Principle

Do not treat this project as a normal utility library.

Symath is intended to become a layered symbolic framework for formal mathematics. Every implementation decision should preserve future extensibility toward:

- symbolic set-theoretic objects
- predicates and membership conditions
- formal logic
- proof objects
- rewrite systems
- mathematical structures
- dependency graphs
- semantic relationships between definitions and theorems

Prefer clear abstractions over clever shortcuts.

---

## Current Development Style

This project is also a learning project. The owner is learning Python deeply while building the system.

When assisting:

- Explain nontrivial changes.
- Prefer small, principled refactors.
- Avoid large unexplained rewrites.
- Do not introduce unnecessary dependencies.
- Keep the code readable to someone still building Python fluency.
- When possible, leave comments explaining conceptual mechanisms, not obvious syntax.

---

## Coding Conventions

Use standard Python naming conventions:

- modules: `snake_case.py`
- classes: `PascalCase`
- functions and methods: `snake_case`
- constants: `UPPER_SNAKE_CASE`

Avoid names like:

```text
rough.py
test.py
random.py
```

unless they are strictly temporary experiments. In particular, avoid naming project modules after standard library modules such as `random.py`, because this can shadow Python's built-in library.

---

## Design Guidelines

Prefer:

- simple classes with explicit responsibilities
- composition over inheritance unless inheritance has a clear mathematical or semantic meaning
- explicit interfaces
- small methods
- readable control flow
- precise error messages
- tests for behavior, not implementation accidents

Avoid:

- global mutable state
- shared mutable defaults
- premature metaclass usage
- deep inheritance hierarchies
- clever dynamic behavior without strong justification
- mixing experimental code with core package code

---

## Mathematical Design Guidelines

When implementing mathematical objects, be precise about whether the object represents:

- a concrete computational value
- a symbolic object
- a predicate
- a definition
- a construction rule
- a formal expression
- a semantic condition
- a proof-relevant dependency

Do not collapse these distinctions casually.

For example, a symbolic set should not merely behave like a Python `set` unless that is explicitly the intended semantics.

---

## Testing Guidelines

Tests should live in `tests/`.

Prefer `pytest`.

Test names should describe behavior:

```python
def test_alphabet_excludes_symbols_from_family():
    ...
```

Instead of:

```python
def test_1():
    ...
```

Tests should focus on externally visible behavior, especially:

- object construction
- membership behavior
- equality semantics
- mutation versus immutability
- symbolic dependency behavior
- edge cases involving empty inputs
- shared mutable state bugs

---

## Refactoring Guidelines

Before refactoring, identify the conceptual role of the file.

Ask:

1. Is this core package code?
2. Is this an experiment?
3. Is this documentation?
4. Is this scratch material?
5. Is this archived historical code?

Do not move archived or experimental code into the core package without making it production-quality.

When renaming or moving files, update imports and tests accordingly.

---

## Documentation Guidelines

Documentation should clarify architecture and concepts, not just usage.

Useful docs include:

- project vision
- architecture notes
- symbolic object model
- logic layer design
- testing notes
- Python learning notes
- glossary of project-specific concepts

Keep documentation close to the current implementation, but do not erase ambitious long-term design notes.

---

## Dependency Policy

Avoid third-party dependencies unless they are clearly justified.

Acceptable early dependencies may include:

- `pytest` for testing
- packaging/build tools
- type-checking tools later, if useful

Do not add heavy symbolic mathematics, theorem proving, or graph libraries prematurely. Symath is intended to build many of its conceptual structures from first principles.

---

## Important Current Warning

The project has already encountered issues involving:

- `__init__` signatures
- class construction
- shared mutable state
- symbolic family instances
- metaclass exploration

Be especially careful around object initialization, class attributes, mutable defaults, and inheritance behavior.

---

## Agent Behavior

When modifying code:

1. Explain the reason for the change.
2. Keep changes minimal.
3. Prefer teaching over replacing.
4. Preserve conceptual clarity.
5. Avoid implementing large new subsystems without explicit direction.
6. Flag design risks.
7. Suggest tests when behavior changes.

This project values understanding over speed.