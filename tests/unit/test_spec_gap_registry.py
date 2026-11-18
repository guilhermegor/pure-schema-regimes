"""Unit tests for ``SpecGapRegistry`` constructor validation (issue #17).

A plain ``str`` value used to be stored as-is, and ``in`` on a string is a substring test, so
``CNPJ`` read as a known gap of ``"CNPJ_FUNDO"``. The constructor now checks every entry.
"""

import pytest

from pure_schema_regimes.spec_gap_registry import SpecGapRegistry


@pytest.mark.parametrize(
    "dict_known_gaps",
    [
        {"old": "CNPJ_FUNDO"},
        {"old": {"CNPJ_FUNDO"}},
        {"old": ["CNPJ_FUNDO"]},
        {"old": frozenset({1})},
        {1: frozenset({"CNPJ_FUNDO"})},
    ],
    ids=["str_value", "set_value", "list_value", "non_str_element", "non_str_key"],
)
def test_spec_gap_registry_bad_entry_raises_type_error(
    dict_known_gaps: dict[object, object],
) -> None:
    """A wrong key, value or element type is refused at construction.

    Parameters
    ----------
    dict_known_gaps : dict[object, object]
        A mapping with exactly one malformed entry.

    Returns
    -------
    None
    """
    with pytest.raises(TypeError):
        SpecGapRegistry(dict_known_gaps)


def test_spec_gap_registry_bad_value_after_good_one_names_the_key() -> None:
    """Every entry is checked, not a sample, and the message names the offending key.

    Returns
    -------
    None
    """
    dict_known_gaps = {"good": frozenset({"A"}), "planted_bad_regime": "CNPJ_FUNDO"}
    with pytest.raises(TypeError, match="planted_bad_regime"):
        SpecGapRegistry(dict_known_gaps)


@pytest.mark.parametrize(
    ("str_column", "bool_expected"),
    [("CNPJ_FUNDO", True), ("CNPJ", False), ("FUNDO", False)],
)
def test_spec_gap_registry_frozenset_matches_whole_column_names_only(
    *, str_column: str, bool_expected: bool
) -> None:
    """A ``frozenset`` value is accepted and matches whole column names, never substrings.

    Parameters
    ----------
    str_column : str
        The column name looked up.
    bool_expected : bool
        Whether it is a registered gap.

    Returns
    -------
    None
    """
    cls_registry = SpecGapRegistry({"old": frozenset({"CNPJ_FUNDO"})})
    assert cls_registry.is_known_gap(str_regime_name="old", str_column=str_column) is bool_expected
