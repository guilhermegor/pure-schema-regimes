# **Usage**

Examples for installing and using this library.

> **See also:** [API Reference](api/index.md)

---

## Installation

```bash
pip install pure-schema-regimes
```

Or with Poetry:

```bash
poetry add pure-schema-regimes
```

The package has no runtime dependencies, so there are no extras.

---

## Basic usage

A published series can change its column set mid-series under one unchanged filename. CVM's
monthly fund profile is keyed by `CNPJ_FUNDO` through period `202311`, and by
`CNPJ_FUNDO_CLASSE` from `202312` on. Declare one window per regime, then resolve a period to
the regime that owns it:

```python
from pure_schema_regimes import RegimeRegistry, RegimeWindow

cls_registry = RegimeRegistry(
    [
        RegimeWindow("cnpj_keyed", int_period_start=None, int_period_end=202311),
        RegimeWindow("cnpj_classe_keyed", int_period_start=202312, int_period_end=None),
    ]
)

cls_registry.resolve(202311).str_name  # "cnpj_keyed"
cls_registry.resolve(202312).str_name  # "cnpj_classe_keyed"
cls_registry.default_period("cnpj_keyed")  # 202311, the closed regime's last period
```

Periods are `YYYYMM` integers. `None` leaves a bound open. Overlapping windows are rejected
when the registry is built, so one period never belongs to two regimes.

---

## Running tests

```bash
poe unit_tests         # unit tests only
poe integration_tests  # integration tests only
poe test_cov           # unit tests + coverage report + badge
```

---

## Linting and formatting

```bash
poe lint          # ruff check + ruff format + codespell + pydocstyle
```

---

## Publishing to PyPI

Two GitHub Actions workflows handle releases (present when the repo has a GitHub remote):

- **`release-test-pypi.yaml`** — publish to [Test PyPI](https://test.pypi.org) first.
- **`release-pypi.yaml`** — publish to [PyPI](https://pypi.org) and cut a GitHub release.

Trigger either from the **Actions** tab (`workflow_dispatch`) with the version to release.
Both gate on the new version being greater than the latest already published, build with
Poetry, and publish through OIDC trusted publishing, so no token secrets are needed.

Configure once, on each index (pypi.org and test.pypi.org), a pending publisher:

- PyPI: workflow `release-pypi.yaml`, environment `release-pypi`.
- Test PyPI: workflow `release-test-pypi.yaml`, environment `release-test-pypi`.

After the first `release-pypi.yaml` run creates the `gh-pages` branch, run `poe enable_pages`
once to serve the docs.
