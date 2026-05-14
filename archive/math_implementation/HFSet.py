from __future__ import annotations
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Any


class HFSet:
    def __init__(self, members: Iterable[HFSet] = ()) -> None:
        checked_members: list[HFSet] = []

        for member in members:
            if not isinstance(member, HFSet):
                raise TypeError("HFSet members must be HFSet instances")
            checked_members.append(member)

        self._members = checked_members



class _SymObj:
    """
    Interned raw syntax object.

    One written mark corresponds to one Python object within the current
    process, so `_SymObj("¬") is _SymObj("¬")`.
    """

    _pool: dict[str, _SymObj] = {}

    def __new__(cls, syntax: object) -> _SymObj:
        text = str(syntax)
        existing = cls._pool.get(text)
        if existing is not None:
            return existing
        obj = super().__new__(cls)
        cls._pool[text] = obj
        return obj

    def __init__(self, syntax: object) -> None:
        if getattr(self, "_initialized", False):
            return
        self.syntax = str(syntax)
        self._initialized = True

    def __repr__(self) -> str:
        return self.syntax

    def __str__(self) -> str:
        return self.syntax

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, _SymObj):
            return NotImplemented
        return self.syntax == other.syntax

    def __hash__(self) -> int:
        return hash(self.syntax)

    @classmethod
    def get(cls, syntax: object) -> _SymObj:
        return cls(syntax)

    @classmethod
    def find(cls, syntax: object) -> _SymObj | None:
        return cls._pool.get(str(syntax))

    @classmethod
    def check(cls, syntax: object) -> bool:
        return str(syntax) in cls._pool

    @classmethod
    def get_all(cls) -> tuple[_SymObj, ...]:
        return tuple(cls._pool.values())


@dataclass
class FieldObservation:
    """What the template has learned about one attribute name."""

    name: str
    seen_count: int = 0
    observed_types: set[str] = field(default_factory=set)
    last_value_repr: str | None = None

    def observe(self, value: Any) -> None:
        self.seen_count += 1
        self.observed_types.add(type(value).__name__)
        self.last_value_repr = repr(value)


class SymTypeTemplate:
    """
    Evolving description of the objects produced by a single `_SymType`.

    The type object stays stable while the template learns the shape of the
    symbols registered through it.
    """

    def __init__(
        self,
        *,
        required_fields: tuple[str, ...] = ("symbolic", "sym_type", "symbol", "label"),
        optional_fields: tuple[str, ...] = ("name", "fields", "parent"),
    ) -> None:
        self.required_fields = required_fields
        self.optional_fields = optional_fields
        self.total_registrations = 0
        self.observations: dict[str, FieldObservation] = {
            name: FieldObservation(name) for name in required_fields + optional_fields
        }
        self.history: list[dict[str, dict[str, Any]]] = []

    def learn(self, obj: _SymTypeObj) -> None:
        self.total_registrations += 1
        current_data = obj.as_template_data()
        for name, value in current_data.items():
            if name not in self.observations:
                self.observations[name] = FieldObservation(name)
            self.observations[name].observe(value)
        self.history.append(self.snapshot())

    def snapshot(self) -> dict[str, dict[str, Any]]:
        return {
            name: {
                "seen_count": obs.seen_count,
                "observed_types": tuple(sorted(obs.observed_types)),
                "last_value_repr": obs.last_value_repr,
            }
            for name, obs in sorted(self.observations.items())
        }

    def inferred_required_fields(self) -> tuple[str, ...]:
        if self.total_registrations == 0:
            return ()
        required = [
            name
            for name, obs in self.observations.items()
            if obs.seen_count == self.total_registrations
        ]
        return tuple(sorted(required))


class Symbolic:
    """Complete internal manager for syntax atoms and symbolic types."""

    def __init__(self) -> None:
        self.defined_types: dict[str, _SymType] = {}

    def intern(self, syntax: object) -> _SymObj:
        return _SymObj.get(syntax)

    def define_type(
        self,
        name: str,
        *,
        parent: _SymType | None = None,
        required_fields: tuple[str, ...] = ("symbolic", "sym_type", "symbol", "label"),
        optional_fields: tuple[str, ...] = ("name", "fields", "parent"),
    ) -> _SymType:
        if name in self.defined_types:
            raise ValueError(f"symbol type {name!r} is already defined")
        sym_type = _SymType(
            symbolic=self,
            name=name,
            parent=parent,
            required_fields=required_fields,
            optional_fields=optional_fields,
        )
        self.defined_types[name] = sym_type
        return sym_type

    def derive_type(
        self,
        name: str,
        parent: _SymType,
        *,
        extra_required_fields: tuple[str, ...] = (),
        extra_optional_fields: tuple[str, ...] = (),
    ) -> _SymType:
        required = tuple(dict.fromkeys(parent.template.required_fields + extra_required_fields))
        optional = tuple(dict.fromkeys(parent.template.optional_fields + extra_optional_fields))
        return self.define_type(
            name,
            parent=parent,
            required_fields=required,
            optional_fields=optional,
        )

    def get_type(self, name: str) -> _SymType:
        return self.defined_types[name]

    def find_type(self, name: str) -> _SymType | None:
        return self.defined_types.get(name)

    def check_type(self, name: str) -> bool:
        return name in self.defined_types

    def get_all_types(self) -> tuple[_SymType, ...]:
        return tuple(self.defined_types.values())

    def define_symbol(
        self,
        type_name: str,
        syntax: object,
        *,
        name: str | None = None,
        fields: tuple[str, ...] = (),
        parent: _SymTypeObj | None = None,
        **attrs: Any,
    ) -> _SymTypeObj:
        sym_type = self.get_type(type_name)
        return sym_type(
            syntax,
            name=name,
            fields=fields,
            parent=parent,
            **attrs,
        )


class _SymType:
    """
    Factory and registry for canonical symbolic objects of a given type.

    `_SymType` is the stable template-like object that a language can keep and
    reuse when defining more symbols of that kind.
    """

    def __init__(
        self,
        *,
        symbolic: Symbolic,
        name: str,
        parent: _SymType | None = None,
        required_fields: tuple[str, ...],
        optional_fields: tuple[str, ...],
    ) -> None:
        self.symbolic = symbolic
        self.name = name
        self.parent = parent
        self.template = SymTypeTemplate(
            required_fields=required_fields,
            optional_fields=optional_fields,
        )
        self._objects_by_symbol: dict[_SymObj, _SymTypeObj] = {}

    def make(
        self,
        syntax: object,
        *,
        name: str | None = None,
        fields: tuple[str, ...] = (),
        parent: _SymTypeObj | None = None,
        **attrs: Any,
    ) -> _SymTypeObj:
        return _SymTypeObj(
            self,
            syntax,
            name=name,
            fields=fields,
            parent=parent,
            **attrs,
        )

    __call__ = make

    def define(
        self,
        syntax: object,
        *,
        name: str | None = None,
        fields: tuple[str, ...] = (),
        parent: _SymTypeObj | None = None,
        **attrs: Any,
    ) -> _SymTypeObj:
        return self.make(
            syntax,
            name=name,
            fields=fields,
            parent=parent,
            **attrs,
        )

    def derive(
        self,
        name: str,
        *,
        extra_required_fields: tuple[str, ...] = (),
        extra_optional_fields: tuple[str, ...] = (),
    ) -> _SymType:
        return self.symbolic.derive_type(
            name,
            self,
            extra_required_fields=extra_required_fields,
            extra_optional_fields=extra_optional_fields,
        )

    def get(self, syntax: object) -> _SymTypeObj | None:
        symbol = self.symbolic.intern(syntax)
        return self._objects_by_symbol.get(symbol)

    find = get

    def require(self, syntax: object) -> _SymTypeObj:
        obj = self.get(syntax)
        if obj is None:
            raise KeyError(f"{syntax!r} is not defined in {self.name}")
        return obj

    def check(self, syntax: object) -> bool:
        return self.get(syntax) is not None

    def get_all(self) -> tuple[_SymTypeObj, ...]:
        return tuple(self._objects_by_symbol.values())

    def __repr__(self) -> str:
        return f"_SymType({self.name!r})"


class _SymTypeObj:
    """
    Canonical typed symbol object.

    The same syntax within one `_SymType` returns the same Python object.
    Repeated construction updates metadata and teaches the template.
    """

    def __new__(
        cls,
        sym_type: _SymType,
        syntax: object,
        *,
        name: str | None = None,
        fields: tuple[str, ...] = (),
        parent: _SymTypeObj | None = None,
        **attrs: Any,
    ) -> _SymTypeObj:
        symbol = sym_type.symbolic.intern(syntax)
        existing = sym_type._objects_by_symbol.get(symbol)
        if existing is not None:
            return existing
        obj = super().__new__(cls)
        sym_type._objects_by_symbol[symbol] = obj
        return obj

    def __init__(
        self,
        sym_type: _SymType,
        syntax: object,
        *,
        name: str | None = None,
        fields: tuple[str, ...] = (),
        parent: _SymTypeObj | None = None,
        **attrs: Any,
    ) -> None:
        symbol = sym_type.symbolic.intern(syntax)
        if getattr(self, "_initialized", False):
            self.refresh(name=name, fields=fields, parent=parent, **attrs)
            self.sym_type.template.learn(self)
            return

        self.symbolic = sym_type.symbolic
        self.sym_type = sym_type
        self.symbol = symbol
        self.label = symbol.syntax
        self.name = name or self.label
        self.fields: tuple[str, ...] = tuple(fields)
        self.parent = parent
        self.extra_attrs: dict[str, Any] = {}
        self._initialized = True
        self.refresh(**attrs)
        self.sym_type.template.learn(self)

    def refresh(
        self,
        *,
        name: str | None = None,
        fields: tuple[str, ...] = (),
        parent: _SymTypeObj | None = None,
        **attrs: Any,
    ) -> None:
        if name is not None:
            self.name = name
        if fields:
            self.fields = tuple(dict.fromkeys(self.fields + tuple(fields)))
        if parent is not None:
            self.parent = parent
        for attr_name, value in attrs.items():
            self.extra_attrs[attr_name] = value
            setattr(self, attr_name, value)

    def as_template_data(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "symbolic": self.symbolic,
            "sym_type": self.sym_type,
            "symbol": self.symbol,
            "label": self.label,
            "name": self.name,
            "fields": self.fields,
            "parent": self.parent,
        }
        data.update(self.extra_attrs)
        return data

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, _SymTypeObj):
            return NotImplemented
        return self.sym_type is other.sym_type and self.symbol is other.symbol

    def __hash__(self) -> int:
        return hash((self.sym_type, self.symbol))

    def __repr__(self) -> str:
        return f"{self.sym_type.name}({self.label!r})"

    def __str__(self) -> str:
        return self.label


class FormalLanguage:
    """
    Thin layer over `Symbolic` for choosing which defined symbols belong to one
    particular language.
    """

    def __init__(self, name: str, symbolic: Symbolic | None = None) -> None:
        self.name = name
        self.symbolic = symbolic or Symbolic()
        self.allowed_types: dict[str, _SymType] = {}
        self.alphabet: dict[str, _SymTypeObj] = {}

    def allow_type(self, sym_type: str | _SymType) -> _SymType:
        resolved = (
            self.symbolic.get_type(sym_type)
            if isinstance(sym_type, str)
            else sym_type
        )
        self.allowed_types[resolved.name] = resolved
        return resolved

    def define_type(
        self,
        name: str,
        *,
        parent: _SymType | None = None,
        required_fields: tuple[str, ...] = ("symbolic", "sym_type", "symbol", "label"),
        optional_fields: tuple[str, ...] = ("name", "fields", "parent"),
    ) -> _SymType:
        sym_type = self.symbolic.define_type(
            name,
            parent=parent,
            required_fields=required_fields,
            optional_fields=optional_fields,
        )
        self.allow_type(sym_type)
        return sym_type

    def derive_type(
        self,
        name: str,
        parent: str | _SymType,
        *,
        extra_required_fields: tuple[str, ...] = (),
        extra_optional_fields: tuple[str, ...] = (),
    ) -> _SymType:
        parent_type = self.allow_type(parent)
        sym_type = parent_type.derive(
            name,
            extra_required_fields=extra_required_fields,
            extra_optional_fields=extra_optional_fields,
        )
        self.allow_type(sym_type)
        return sym_type

    def define_symbol(
        self,
        sym_type: str | _SymType,
        syntax: object,
        *,
        name: str | None = None,
        fields: tuple[str, ...] = (),
        parent: _SymTypeObj | None = None,
        **attrs: Any,
    ) -> _SymTypeObj:
        resolved = self.allow_type(sym_type)
        symbol = resolved(
            syntax,
            name=name,
            fields=fields,
            parent=parent,
            **attrs,
        )
        self.alphabet[symbol.label] = symbol
        return symbol

    def include(self, symbol: _SymTypeObj) -> None:
        self.allow_type(symbol.sym_type)
        self.alphabet[symbol.label] = symbol

    def get_symbol(self, syntax: object) -> _SymTypeObj | None:
        return self.alphabet.get(str(syntax))

    find_symbol = get_symbol

    def has_symbol(self, syntax: object) -> bool:
        return str(syntax) in self.alphabet

    def get_symbols(self) -> tuple[_SymTypeObj, ...]:
        return tuple(self.alphabet.values())

    def get_type(self, name: str) -> _SymType:
        return self.symbolic.get_type(name)

