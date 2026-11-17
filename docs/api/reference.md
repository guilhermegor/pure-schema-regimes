# **API Reference**

Public interface for this library.

> **See also:** [Usage](../usage.md)

---

## Public classes

Import all four from the package root: `from pure_schema_regimes import RegimeWindow`.

| Class | Role |
|-------|------|
| `RegimeWindow` | Frozen value object: a regime's name and the `YYYYMM` periods it covers (`None` leaves a bound open). Rejects a malformed period or a backwards range. |
| `RegimeRegistry` | Maps a period to the one window that covers it (`resolve`), and gives a closed regime's last period (`default_period`). Rejects overlapping windows. |
| `RegimeBoundAdapter` | Binds one adapter to one regime and refuses a period that belongs to another. Carries no I/O: a concrete reader composes or subclasses it. |
| `SpecGapRegistry` | A named list of expected `(regime, column)` gaps between a closed regime and a spec written for the current one (`is_known_gap`, `unexplained`). |

See [Usage](../usage.md) and [Examples](../examples.md) for the CVM fund-profile case these
classes were measured against.

---

## Adding new modules

Place new modules under `src/<package_name>/`. Export public symbols from `src/<package_name>/__init__.py` so callers can do:

```python
from <package_name> import my_function
```

Follow the one-class-per-file convention: utility functions with no shared state belong at module level, not wrapped in a class.

---

## Conventions

| Convention | Rule |
|------------|------|
| Type hints | Required on all public functions, including `-> None` return types |
| Docstrings | NumPy style; explain *why*, not *what* |
| Variable names | Type-prefixed (`str_`, `list_`, `cls_`, `dict_`, …) |
| Testing | `unittest`; one assertion per test; name as `test_<unit>_<scenario>_<expected>` |
