from __future__ import annotations

from garbage.math_implementation.HFSet import FormalLanguage, Symbolic, _SymObj


def test_raw_syntax_is_interned() -> None:
    neg_1 = _SymObj("¬")
    neg_2 = _SymObj("¬")

    assert neg_1 is neg_2
    assert str(neg_1) == "¬"


def test_same_syntax_returns_same_typed_object() -> None:
    symbolic = Symbolic()
    variable = symbolic.define_type("Variable")

    x1 = variable("x")
    x2 = variable("x")

    assert x1 is x2
    assert x1 == x2
    assert hash(x1) == hash(x2)


def test_repeated_construction_teaches_template() -> None:
    symbolic = Symbolic()
    connective = symbolic.define_type("Connective")

    neg = connective("¬", name="negation")
    assert neg.fields == ()

    neg_again = connective(
        "¬",
        fields=("formula",),
        arity=1,
        notation="prefix",
    )

    assert neg_again is neg
    assert neg.fields == ("formula",)
    assert neg.arity == 1
    assert neg.notation == "prefix"

    snapshot = connective.template.snapshot()
    assert snapshot["arity"]["seen_count"] == 1
    assert snapshot["arity"]["observed_types"] == ("int",)
    assert snapshot["notation"]["observed_types"] == ("str",)


def test_template_tracks_history_over_time() -> None:
    symbolic = Symbolic()
    operation = symbolic.define_type("Operation")

    operation("mul")
    operation("mul", fields=("left", "right"), associative=True)
    operation("unit", fields=("identity",), nullary=False)

    history = operation.template.history
    assert len(history) == 3
    assert "associative" not in history[0]
    assert "associative" in history[1]
    assert "nullary" in history[2]


def test_registry_is_per_sym_type() -> None:
    symbolic = Symbolic()
    variable = symbolic.define_type("Variable")
    constant = symbolic.define_type("Constant")

    x_variable = variable("x")
    x_constant = constant("x")

    assert x_variable is not x_constant
    assert x_variable != x_constant
    assert repr(x_variable) == "Variable('x')"
    assert repr(x_constant) == "Constant('x')"


def test_type_can_be_derived_from_existing_type() -> None:
    symbolic = Symbolic()
    connective = symbolic.define_type("Connective")
    sentential = connective.derive(
        "SententialConnective",
        extra_optional_fields=("arity",),
    )

    neg = sentential("¬", arity=1)

    assert symbolic.get_type("SententialConnective") is sentential
    assert sentential.parent is connective
    assert neg.arity == 1


def test_language_can_define_types_and_symbols() -> None:
    language = FormalLanguage("Sentential Logic")
    connective = language.define_type("Connective")
    language.define_symbol(connective, "¬", name="negation", arity=1)
    language.define_symbol(connective, "∨", name="disjunction", arity=2)

    assert language.has_symbol("¬")
    assert language.get_symbol("∨").name == "disjunction"
    assert tuple(sym.label for sym in language.get_symbols()) == ("¬", "∨")


def run_all_tests() -> None:
    tests = [
        test_raw_syntax_is_interned,
        test_same_syntax_returns_same_typed_object,
        test_repeated_construction_teaches_template,
        test_template_tracks_history_over_time,
        test_registry_is_per_sym_type,
        test_type_can_be_derived_from_existing_type,
        test_language_can_define_types_and_symbols,
    ]
    for test in tests:
        test()
    print(f"ran {len(tests)} tests successfully")


if __name__ == "__main__":
    run_all_tests()
