"""Per-regime schema adapters for series that change columns mid-series."""

from importlib.metadata import PackageNotFoundError, version

from .regime_adapter import RegimeBoundAdapter
from .regime_registry import RegimeRegistry
from .regime_window import RegimeWindow
from .spec_gap_registry import SpecGapRegistry


try:
    __version__ = version("pure-schema-regimes")
except PackageNotFoundError:  # pragma: no cover - source tree without an installed dist
    __version__ = "0.0.0"


__all__ = [
    "__version__",
    "RegimeBoundAdapter",
    "RegimeRegistry",
    "RegimeWindow",
    "SpecGapRegistry",
]
