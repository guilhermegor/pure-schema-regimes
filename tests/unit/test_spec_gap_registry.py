"""Unit tests for ``SpecGapRegistry`` constructor validation (issue #17).

A plain ``str`` value used to be stored as-is, and ``in`` on a string is a substring test, so
``CNPJ`` read as a known gap of ``"CNPJ_FUNDO"``. The constructor now checks every entry.
"""

from collections.abc import Callable
import copy
import pickle  # noqa: S403 - round-trips an object this test builds itself

import pytest

from pure_schema_regimes.spec_gap_registry import SpecGapRegistry


@pytest.mark.parametrize(
    ("dict_known_gaps", "str_match"),
    [
        ({"old": "CNPJ_FUNDO"}, "must be frozenset"),
        ({"old": {"CNPJ_FUNDO"}}, "must be frozenset"),
        ({"old": ["CNPJ_FUNDO"]}, "must be frozenset"),
        ({"old": frozenset({1})}, "must contain only str"),
        ({1: frozenset({"CNPJ_FUNDO"})}, "regime name 1 must be str"),
    ],
    ids=["str_value", "set_value", "list_value", "non_str_element", "non_str_key"],
)
def test_spec_gap_registry_bad_entry_raises_type_error(
    *, dict_known_gaps: dict[object, object], str_match: str
) -> None:
    """A wrong key, value or element type is refused by this module's own validators.

    Parameters
    ----------
    dict_known_gaps : dict[object, object]
        A mapping with exactly one malformed entry.
    str_match : str
        A phrase only this module's validators raise.

    Returns
    -------
    None
    """
    with pytest.raises(TypeError, match=str_match):
        SpecGapRegistry(dict_known_gaps)  # type: ignore[arg-type]


def test_spec_gap_registry_mutating_source_dict_after_init_changes_nothing() -> None:
    """The registry keeps a copy, so a later bad write to the caller's dict cannot reach it.

    Returns
    -------
    None
    """
    dict_known_gaps: dict[str, object] = {"old": frozenset({"OTHER"})}
    cls_registry = SpecGapRegistry(dict_known_gaps)  # type: ignore[arg-type]
    dict_known_gaps["old"] = "CNPJ_FUNDO"
    assert cls_registry.is_known_gap(str_regime_name="old", str_column="CNPJ") is False


def test_spec_gap_registry_known_gaps_view_is_read_only() -> None:
    """The stored mapping refuses writes, so no unvalidated entry can be added later.

    Returns
    -------
    None
    """
    cls_registry = SpecGapRegistry({"old": frozenset({"A"})})
    with pytest.raises(TypeError):
        cls_registry.dict_known_gaps["old"] = "CNPJ_FUNDO"  # type: ignore[index]


def test_spec_gap_registry_bad_value_after_good_one_names_the_key() -> None:
    """Every entry is checked, not a sample, and the message names the offending key.

    Returns
    -------
    None
    """
    dict_known_gaps = {"good": frozenset({"A"}), "planted_bad_regime": "CNPJ_FUNDO"}
    with pytest.raises(TypeError, match="planted_bad_regime"):
        SpecGapRegistry(dict_known_gaps)  # type: ignore[arg-type]


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


@pytest.mark.parametrize(
    "fn_round_trip",
    [lambda obj: pickle.loads(pickle.dumps(obj)), copy.deepcopy],  # noqa: S301
    ids=["pickle", "deepcopy"],
)
def test_spec_gap_registry_round_trip_keeps_known_gaps(
    fn_round_trip: Callable[[SpecGapRegistry], SpecGapRegistry],
) -> None:
    """A registry survives pickle and deepcopy with its gaps intact.

    Parameters
    ----------
    fn_round_trip : Callable[[SpecGapRegistry], SpecGapRegistry]
        Serialises and restores, or deep-copies, the registry.

    Returns
    -------
    None
    """
    cls_registry = fn_round_trip(SpecGapRegistry({"old": frozenset({"CNPJ_FUNDO"})}))
    assert dict(cls_registry.dict_known_gaps) == {"old": frozenset({"CNPJ_FUNDO"})}


def test_spec_gap_registry_known_gaps_cannot_be_rebound() -> None:
    """The public attribute is a read-only property, so rebinding it cannot skip validation.

    Returns
    -------
    None
    """
    cls_registry = SpecGapRegistry({"old": frozenset({"A"})})
    with pytest.raises(AttributeError):
        cls_registry.dict_known_gaps = {"old": "CNPJ_FUNDO"}  # type: ignore[misc, dict-item]


def test_spec_gap_registry_empty_frozenset_value_has_no_known_gaps() -> None:
    """An empty ``frozenset`` is a valid entry that registers no gap.

    Returns
    -------
    None
    """
    cls_registry = SpecGapRegistry({"old": frozenset()})
    assert cls_registry.is_known_gap(str_regime_name="old", str_column="CNPJ") is False
