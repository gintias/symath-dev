from __future__ import annotations
from collections.abc import Iterable, Iterator, Mapping
from types import MappingProxyType
from collections.abc import Iterable, Callable
import builtins
import inspect
from typing import Any
import types



class Symbol:

    def __init__(self, name: str, symbol: str, symbol_type: str | None = None):
        super().__setattr__("_name", name)
        super().__setattr__("_symbol", symbol)
        super().__setattr__("_symbol_type", symbol_type)
        super().__setattr__("_frozen", True)

    def __setattr__(self, name, value):
        if getattr(self, "_frozen", False):
            raise AttributeError(f"{type(self).__name__} objects are immutable")
        super().__setattr__(name, value)
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        
        return self._symbol == other._symbol
    
    def __str__(self) -> str:
        return self._symbol
    
    def __hash__(self) -> int:
        return hash((type(self), self._symbol))


class Parenthesis(Symbol):

    def __init__(self, name: str, symbol: str, side: str):
        super().__init__(name, symbol, symbol_type = type(self).__name__)
        object.__setattr__(self, "_side", side)

class SententialConnective(Symbol):

    def __init__(self, name: str, symbol: str, arity: int):
        super().__init__(name, symbol, symbol_type = type(self).__name__)
        object.__setattr__(self, "_arity", arity)

class SentenceSymbol(Symbol):

    def __init__(self, name: str, symbol: str):
        super().__init__(name, symbol, symbol_type = type(self).__name__)


class LogicalConstant(Symbol):

    def __init__(self, name: str, symbol: str):
        super().__init__(name, symbol, symbol_type = type(self).__name__)
    

print(LogicalConstant.__name__)
class FiniteSymbolFamily:
    def __init__(self):
        self._family_symbol_type = None
        self._cache = {}
        self._family = set()
        self._sym_count = 0

    def set_from(
        self,
        items: Iterable[str] | Iterable[Symbol],
        *,
        symbol_type: type[Symbol] | None = None,
        factory: Callable[[str, int], Symbol] | None = None,
    ):
        """
        Set this finite family from either:

        1. Symbol objects:
           set_from([NOT, AND, OR], symbol_type=SententialConnective)

        2. Strings:
           set_from(["P", "Q", "R"], symbol_type=SentenceSymbol)

        For strings, either symbol_type must be supplied or factory must be supplied.
        """

        # Important: strings themselves are iterable character-by-character,
        # so reject a bare string.
        if isinstance(items, str):
            raise TypeError("set_from expects an iterable of strings, not one bare string")

        items = list(items)

        # Empty family case
        if not items:
            if symbol_type is not None:
                self._family_symbol_type = symbol_type

            self._cache = {}
            self._family = set()
            self._sym_count = 0
            return self

        all_symbols = all(isinstance(item, Symbol) for item in items)
        all_strings = all(isinstance(item, str) for item in items)

        if not all_symbols and not all_strings:
            raise TypeError(
                "items must be either all Symbol objects or all strings"
            )

        if all_symbols:
            symbols = items

            if symbol_type is None:
                symbol_type = type(symbols[0])

            for symbol in symbols:
                if not isinstance(symbol, symbol_type):
                    raise TypeError(
                        f"Expected symbols of type {symbol_type.__name__}, "
                        f"got {type(symbol).__name__}"
                    )

        else:
            # all_strings case
            raw_symbols = items

            if symbol_type is None and self._family_symbol_type is None and factory is None:
                raise TypeError(
                    "When setting from strings, provide symbol_type or factory"
                )

            if symbol_type is None:
                symbol_type = self._family_symbol_type

            if factory is None:
                def factory(raw_symbol: str, index: int) -> Symbol:
                    return symbol_type(
                        name=f"{symbol_type.__name__} #{index}",
                        symbol=raw_symbol,
                    )

            symbols = [
                factory(raw_symbol, index)
                for index, raw_symbol in enumerate(raw_symbols)
            ]

            for symbol in symbols:
                if not isinstance(symbol, Symbol):
                    raise TypeError(
                        "factory must return Symbol objects"
                    )

                if symbol_type is not None and not isinstance(symbol, symbol_type):
                    raise TypeError(
                        f"factory returned {type(symbol).__name__}, "
                        f"expected {symbol_type.__name__}"
                    )

        self._family_symbol_type = symbol_type
        self._cache = {
            index: symbol
            for index, symbol in enumerate(symbols)
        }
        self._family = set(symbols)
        self._sym_count = len(symbols)

        return self

    def __len__(self):
        return self._sym_count

    def __iter__(self):
        return iter(self._cache.values())

    def __contains__(self, symbol):
        return symbol in self._family

    def __getitem__(self, index: int):
        if index < 0:
            raise IndexError("negative indices are not supported")
        return self._cache[index]

    def __str__(self):
        items = ", ".join(str(self._cache[i]) for i in sorted(self._cache))
        return "{" + items + "}"
                

class CountableSymbolFamily:

    def __init__(self, symbol_type: type[Symbol], prefix: str = "A"):
        self._symbol_type = symbol_type
        self._prefix = prefix
        self._count = 0
        self._cache: dict[int, Symbol] = {}

    def __len__(self) -> int:
        return self._count
    
    def __iter__(self) -> Iterator[Symbol]:
        return iter(self._cache.values())
    
    def __contains__(self, symbol: object) -> bool:
        return self._index_of(symbol) is not None

    def _index_of(self, symbol: object) -> int | None:
        if not isinstance(symbol, self._symbol_type):
            return None

        prefix, separator, suffix = symbol._symbol.partition("_")
        if (
            prefix != self._prefix
            or separator != "_"
            or not suffix.isdecimal()
            or suffix != str(int(suffix))
        ):
            return None
        return int(suffix)

    def _make_symbol(self, index: int) -> Symbol:
        symbol_syntax = f"{self._prefix}_{index}"
        symbol_name = f"{self._symbol_type.__name__} #{index}"
        return self._symbol_type(symbol_name, symbol_syntax)

    def _add_symbols(self, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError(f"Quantity must be positive")
        
        for _ in range(quantity):
            index = self._count
            self._cache[index] = self._make_symbol(index)
            self._count += 1

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._symbol_type is other._symbol_type and self._prefix == other._prefix
    
    def __str__(self) -> str:
        items = ", ".join(str(self._cache[i]) for i in sorted(self._cache))
        return "{" + items + ", ...}"
    
    def __getitem__(self, index: int) -> Symbol:
        if not isinstance(index, int) or isinstance(index, bool):
            raise TypeError("index must be an integer")
        if index < 0:
            raise IndexError("negative indices are not supported")
        if index >= self._count:
            self._add_symbols(index - self._count + 1)
        return self._cache[index]
    
    def __hash__(self) -> int:
        return hash((type(self), self._symbol_type, self._prefix))
    

class Alphabet:
    # Fixed sentential logic symbols
    LPAREN = Parenthesis("left parenthesis", "(", "left")
    RPAREN = Parenthesis("right parenthesis", ")", "right")

    NOT = SententialConnective("negation", "¬", 1)
    AND = SententialConnective("conjunction", "∧", 2)
    OR = SententialConnective("disjunction", "∨", 2)
    IMPLIES = SententialConnective("conditional", "→", 2)
    IFF = SententialConnective("biconditional", "↔", 2)

    TRUTHIFY= LogicalConstant("truthify", "⊤")
    FALSIFY = LogicalConstant("truthify", "⊥")
    
    PARENTHESES = frozenset({LPAREN, RPAREN})
    BASIC_CONNECTIVES = frozenset({NOT, AND, OR})
    CONDITIONAL_CONNECTIVES = frozenset({IMPLIES, IFF})
    LOGICAL_CONSTANTS = frozenset({TRUTHIFY, FALSIFY})

    # Fixed groups
    FINITE_SYM_TYPES = {
        "parentheses" : PARENTHESES,
        "basic_connectives" : BASIC_CONNECTIVES,
        "conditional_connectives" : CONDITIONAL_CONNECTIVES,
        "logical_constants" :  LOGICAL_CONSTANTS
    }

    INFINITE_SYM_TYPES = {
        "sentence_symbols" : CountableSymbolFamily(SentenceSymbol, prefix="A")
    }

    PRESETS = {
        "sentential_logic" : {

            "fixed_groups" : {
                "parentheses",
                "basic_connectives",
                "conditional_connectives",
               "logical_constants",},

            "families" : {"SentenceSymbol": CountableSymbolFamily(SentenceSymbol, prefix="A"),}
            }
            }

    def __init__(self, *, preset = None, include = "all", exclude = None):
        pass




class Test:
    _vars = []

    @classmethod
    def add_var(cls, var):
        cls._vars.append(var)

    @classmethod
    def get_vars(cls):
        return cls._vars
    

T = Test()
T.add_var(3)
print(T.get_vars())
