# **API Reference**

Public interface for this library.

> **See also:** [Usage](../usage.md)

---

## Public classes

Import all four from the package root: `from pure_schema_regimes import RegimeWindow`. The
package also exports `__version__`, the installed distribution's version.

| Class | Role |
|-------|------|
| `RegimeWindow` | Frozen value object: a regime's name and the `YYYYMM` periods it covers (`None` leaves a bound open). Rejects a malformed period or a backwards range. |
| `RegimeRegistry` | Maps a period to the one window that covers it (`resolve`), and gives a closed regime's last period (`default_period`). Rejects overlapping windows. |
| `RegimeBoundAdapter` | Binds one adapter to one regime and refuses a period that belongs to another. Carries no I/O: a concrete reader composes or subclasses it. |
| `SpecGapRegistry` | A named list of expected `(regime, column)` gaps between a closed regime and a spec written for the current one (`is_known_gap`, `unexplained`). Takes any `Mapping` of `str` to `frozenset[str]`, refusing anything else with `TypeError`, and keeps a private copy; `dict_known_gaps` is a read-only view. |

See [Usage](../usage.md) and [Examples](../examples.md) for the CVM fund-profile case these
classes were measured against.

---

## Conventions

| Convention | Rule |
|------------|------|
| Type hints | Required on all public functions, including `-> None` return types |
| Docstrings | NumPy style; explain *why*, not *what* |
| Variable names | Type-prefixed (`str_`, `list_`, `cls_`, `dict_`, …) |
| Testing | `pytest` functions; one assertion per unit test; name as `test_<unit>_<scenario>_<expected>` |
