"""Unit tests: ``RegimeBoundAdapter`` composes with a consumer's own metaclass (#16).

A BlueprintX-scaffolded consumer writes ``class Reader(RegimeBoundAdapter,
metaclass=TypeChecker)`` with its OWN project ``TypeChecker``. The base must not carry an
unrelated metaclass, or class creation raises ``TypeError: metaclass conflict``.
"""

from abc import ABCMeta

import pytest

from pure_schema_regimes.regime_adapter import RegimeBoundAdapter
from pure_schema_regimes.regime_registry import RegimeRegistry
from pure_schema_regimes.regime_window import RegimeWindow


class _ConsumerTypeChecker(ABCMeta):
    """Stand-in for a consumer project's own ``ABCMeta``-derived ``TypeChecker``."""


class _ConsumerReader(RegimeBoundAdapter, metaclass=_ConsumerTypeChecker):
    """A per-regime reader declared the way a scaffolded consumer declares one."""


@pytest.fixture
def cls_registry() -> RegimeRegistry:
    """Build the two-regime registry from the measured cutover (202311 / 202312).

    Returns
    -------
    RegimeRegistry
        The legacy ``cnpj_keyed`` regime (closed at ``202311``) and the current
        ``cnpj_classe_keyed`` regime (open from ``202312``).
    """
    return RegimeRegistry(
        [
            RegimeWindow(str_name="cnpj_keyed", int_period_start=None, int_period_end=202311),
            RegimeWindow(
                str_name="cnpj_classe_keyed", int_period_start=202312, int_period_end=None
            ),
        ]
    )


def test_subclass_with_its_own_abcmeta_metaclass_is_created(
    cls_registry: RegimeRegistry,
) -> None:
    """A consumer subclass passing its own ``ABCMeta``-derived metaclass builds and binds.

    Parameters
    ----------
    cls_registry : RegimeRegistry
        The two-regime fixture registry.

    Returns
    -------
    None
    """
    cls_reader = _ConsumerReader(cls_registry=cls_registry, str_regime_name="cnpj_keyed")
    assert cls_reader.int_period == 202311


def test_consumer_subclass_still_refuses_a_period_from_another_regime(
    cls_registry: RegimeRegistry,
) -> None:
    """The refusal survives the metaclass change, through a consumer subclass too.

    Parameters
    ----------
    cls_registry : RegimeRegistry
        The two-regime fixture registry.

    Returns
    -------
    None
    """
    with pytest.raises(ValueError, match="cnpj_classe_keyed"):
        _ConsumerReader(cls_registry=cls_registry, str_regime_name="cnpj_keyed", int_period=202312)


def test_badly_typed_constructor_call_raises_type_error(cls_registry: RegimeRegistry) -> None:
    """The runtime type check still guards the constructor without the metaclass.

    A non-``str`` regime name would otherwise fall through to the regime comparison and
    surface as a misleading ``ValueError``.

    Parameters
    ----------
    cls_registry : RegimeRegistry
        The two-regime fixture registry.

    Returns
    -------
    None
    """
    with pytest.raises(TypeError, match="str_regime_name"):
        RegimeBoundAdapter(
            cls_registry=cls_registry,
            str_regime_name=42,  # type: ignore[arg-type]
        )
