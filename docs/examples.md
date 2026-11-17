# **Examples**

Task-oriented, self-contained snippets for common uses of this library. Each recipe stands
alone — copy it and adjust.

> **See also:** [Usage](usage.md) for the basics · [API Reference](api/index.md) for every public
> symbol.

---

Every recipe uses the same two-regime registry, CVM's monthly fund profile:

```python
from pure_schema_regimes import RegimeRegistry, RegimeWindow

cls_registry = RegimeRegistry(
    [
        RegimeWindow("cnpj_keyed", int_period_start=None, int_period_end=202311),
        RegimeWindow("cnpj_classe_keyed", int_period_start=202312, int_period_end=None),
    ]
)
```

## Recipe: bind a reader to one regime

Subclass or compose `RegimeBoundAdapter` in each per-regime reader. It refuses a period that
belongs to another regime, so a reader written for the old columns is never handed a file in
the new layout.

```python
from pure_schema_regimes import RegimeBoundAdapter

# No period given: a closed regime defaults to its own last period, not to "today".
cls_adapter = RegimeBoundAdapter(cls_registry=cls_registry, str_regime_name="cnpj_keyed")
cls_adapter.int_period  # 202311

RegimeBoundAdapter(cls_registry=cls_registry, str_regime_name="cnpj_keyed", int_period=202401)
# ValueError: Period 202401 belongs to regime 'cnpj_classe_keyed', not 'cnpj_keyed'.
```

## Recipe: suppress known spec gaps, and only those

A metadata spec written for the current regime reports the old regime's missing columns on
every run. Register each confirmed gap by name instead of turning the check off, so a new,
unexpected column still fails.

```python
from pure_schema_regimes import SpecGapRegistry

cls_gaps = SpecGapRegistry({"cnpj_keyed": frozenset({"CNPJ_FUNDO_CLASSE", "TP_FUNDO_CLASSE"})})

cls_gaps.unexplained(
    str_regime_name="cnpj_keyed",
    set_reported_columns=frozenset({"CNPJ_FUNDO_CLASSE", "TP_FUNDO_CLASSE", "VL_NOVO"}),
)
# frozenset({"VL_NOVO"}): the one column nobody has explained
```
