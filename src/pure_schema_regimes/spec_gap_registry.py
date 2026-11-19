"""Narrow, named registry of expected spec-vs-regime column gaps.

Part of the per-regime adapter pattern (blueprintx#148), the checklist item nothing else in the
pattern delivers: "a spec documenting only the current regime is not an oracle for the
historical one". A drift/oracle check that compares a closed regime's actual columns against
a metadata spec written for the CURRENT regime will report every column the two regimes
disagree on, forever — and the fix is never a blanket suppression of that comparison, because
that would also hide a genuinely new, unexpected mismatch the same check exists to catch.

:class:`SpecGapRegistry` narrows the suppression to exactly the ``(regime, column)`` pairs a
human has confirmed are an *expected* historical gap, named individually. Everything not
listed is reported as before — "the adapter's other oracle still running", in the issue's own
words: registering one known gap changes nothing about how any other column is checked.
"""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType

from pure_schema_regimes._internal.utils.typing import TypeChecker, type_checker


@type_checker
def _require_mapping(*, obj_known_gaps: object) -> None:
    """Raise ``TypeError`` unless the constructor argument is a ``Mapping``.

    Without this, ``dict()`` would accept a list of pairs, and a string or ``None`` would
    fail with ``ValueError`` or a builtin ``TypeError`` instead of this module's own.

    Parameters
    ----------
    obj_known_gaps : object
        The constructor argument.

    Raises
    ------
    TypeError
        When the argument is not a ``Mapping``.
    """
    if not isinstance(obj_known_gaps, Mapping):
        raise TypeError(
            f"known gaps must be a mapping of str to frozenset[str], "
            f"got {type(obj_known_gaps).__name__}"
        )


@type_checker
def _require_str_key(*, obj_regime_name: object) -> None:
    """Raise ``TypeError`` unless the regime name is a ``str``.

    Parameters
    ----------
    obj_regime_name : object
        The mapping key.

    Raises
    ------
    TypeError
        When the key is not a ``str``.
    """
    if not isinstance(obj_regime_name, str):
        raise TypeError(
            f"regime name {obj_regime_name!r} must be str, got {type(obj_regime_name).__name__}"
        )


@type_checker
def _require_frozenset_value(*, obj_regime_name: object, obj_columns: object) -> None:
    """Raise ``TypeError`` unless the known-gap value is a ``frozenset``.

    A plain ``str`` value is the defect this guards (issue #17): ``in`` on a string is a
    substring test, so ``CNPJ`` would read as a known gap of ``"CNPJ_FUNDO"``. A mutable
    ``set`` is refused too, so the registry cannot change after construction.

    Parameters
    ----------
    obj_regime_name : object
        The mapping key, named in the error.
    obj_columns : object
        The mapping value.

    Raises
    ------
    TypeError
        When the value is not a ``frozenset``.
    """
    if not isinstance(obj_columns, frozenset):
        raise TypeError(
            f"known gaps for regime {obj_regime_name!r} must be frozenset[str], "
            f"got {type(obj_columns).__name__}"
        )


@type_checker
def _require_str_columns(*, obj_regime_name: object, set_columns: frozenset[object]) -> None:
    """Raise ``TypeError`` unless every column name in the value is a ``str``.

    Parameters
    ----------
    obj_regime_name : object
        The mapping key, named in the error.
    set_columns : frozenset of object
        The mapping value, already known to be a ``frozenset``.

    Raises
    ------
    TypeError
        When any element is not a ``str``.
    """
    list_bad = sorted(
        f"{obj_column!r} ({type(obj_column).__name__})"
        for obj_column in set_columns
        if not isinstance(obj_column, str)
    )
    if list_bad:
        raise TypeError(
            f"known gaps for regime {obj_regime_name!r} must contain only str, "
            f"got {', '.join(list_bad)}"
        )


class SpecGapRegistry(metaclass=TypeChecker):
    """Look up whether a ``(regime, column)`` pair is a known, expected spec gap.

    Parameters
    ----------
    dict_known_gaps : Mapping of str to frozenset of str
        Regime name → the column names that regime is KNOWN to lack in the current spec.
        Any ``Mapping`` is accepted (a ``dict``, a ``MappingProxyType``, ...). A regime
        absent from this mapping has no known gaps (every mismatch is reported).

    Raises
    ------
    TypeError
        When the argument is not a ``Mapping``, a key is not ``str``, a value is not
        ``frozenset``, or a value holds a non-``str`` element. Every entry is checked here because ``TypeChecker`` skips
        dunder methods, so nothing else validates the constructor's argument.

    Notes
    -----
    The constructor copies the mapping first and validates the copy, so a later write to
    the caller's mapping cannot reach the registry. Storage is a private ``dict``, which keeps
    the registry picklable; the public ``dict_known_gaps`` is a read-only property.
    """

    def __init__(self, dict_known_gaps: Mapping[str, frozenset[str]]) -> None:
        _require_mapping(obj_known_gaps=dict_known_gaps)
        dict_copy = dict(dict_known_gaps)
        for obj_regime_name, obj_columns in dict_copy.items():
            _require_str_key(obj_regime_name=obj_regime_name)
            _require_frozenset_value(obj_regime_name=obj_regime_name, obj_columns=obj_columns)
            _require_str_columns(obj_regime_name=obj_regime_name, set_columns=obj_columns)
        self._dict_known_gaps = dict_copy

    @property
    def dict_known_gaps(self) -> Mapping[str, frozenset[str]]:
        """Read-only view of the validated known gaps.

        Returns
        -------
        Mapping[str, frozenset[str]]
            A live, write-refusing view over the private copy built at construction.
        """
        return MappingProxyType(self._dict_known_gaps)

    @type_checker
    def is_known_gap(self, *, str_regime_name: str, str_column: str) -> bool:
        """Return whether ``str_column`` is a registered, expected gap for the regime.

        Parameters
        ----------
        str_regime_name : str
            The regime whose spec is being compared.
        str_column : str
            The column name the comparison reported as missing from the spec.

        Returns
        -------
        bool
            ``True`` only when this exact pair was registered — never for an unlisted
            column, however similar, and never for an unlisted regime.
        """
        return str_column in self._dict_known_gaps.get(str_regime_name, frozenset())

    @type_checker
    def unexplained(  # complexity-ok: filtering by membership is the narrowing itself
        self, *, str_regime_name: str, set_reported_columns: frozenset[str]
    ) -> frozenset[str]:
        """Narrow a reported set of "not in spec" columns to the genuinely unexplained ones.

        This is the seam that keeps the oracle running: pass it every column a drift/oracle
        check flagged for the regime, and only the ones NOT covered by a registered gap come
        back — so a caller can suppress the known gaps while still failing on anything new.

        Parameters
        ----------
        str_regime_name : str
            The regime the columns were reported against.
        set_reported_columns : frozenset of str
            Columns a comparison reported as missing from the spec.

        Returns
        -------
        frozenset of str
            The subset of ``set_reported_columns`` with no registered gap entry — empty
            when every reported column is an expected, registered gap.
        """
        return frozenset(
            str_column
            for str_column in set_reported_columns
            if not self.is_known_gap(str_regime_name=str_regime_name, str_column=str_column)
        )
