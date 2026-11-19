<!-- readme-archetype: library -->
# pure-schema-regimes

<p align="center"><img src="https://raw.githubusercontent.com/guilhermegor/pure-schema-regimes/main/docs/assets/logo.png" width="200" alt="pure-schema-regimes logo"></p>

[![Project Status: Active](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)
[![PyPI](https://img.shields.io/pypi/v/pure-schema-regimes.svg)](https://pypi.org/project/pure-schema-regimes/)
[![Downloads](https://img.shields.io/pepy/dt/pure-schema-regimes)](https://pepy.tech/projects/pure-schema-regimes)
[![Docs](https://img.shields.io/badge/docs-latest-blue.svg)](https://guilhermegor.github.io/pure-schema-regimes/)
[![Linting](https://img.shields.io/badge/linting-ruff_%7C_codespell-blue)](https://github.com/astral-sh/ruff)
[![Mypy](https://img.shields.io/badge/type--checked-mypy-blue)](https://mypy-lang.org)
![Test Coverage](https://raw.githubusercontent.com/guilhermegor/pure-schema-regimes/badges/coverage.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Open Issues](https://img.shields.io/github/issues/guilhermegor/pure-schema-regimes)
![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-darkgreen.svg)

<!-- slug: overview -->
## Overview

Per-regime schema adapters for series that change columns mid-series (zero-dependency)

A published series can change its column set mid-series under one unchanged filename. CVM's
monthly fund profile is keyed by `CNPJ_FUNDO` through period `202311` and by
`CNPJ_FUNDO_CLASSE` from `202312` on, with the other columns unchanged. Deriving one contract
from the other is right about almost every column and silently wrong about the one that
matters. This package gives each regime its own window and refuses a period that belongs to
another regime. It does no I/O: your readers stay yours.

<!-- slug: features -->
## Features

- `RegimeWindow`: the `YYYYMM` periods one regime covers, with open bounds.
- `RegimeRegistry`: resolves a period to the one regime that owns it, and rejects overlaps.
- `RegimeBoundAdapter`: binds a reader to one regime and refuses another regime's period.
- `SpecGapRegistry`: suppresses named, expected spec gaps while still reporting new ones.
- Zero runtime dependencies: standard library only.

<!-- slug: documentation -->
## Documentation

The documentation site lives at https://guilhermegor.github.io/pure-schema-regimes/. Serve it locally with `poetry run poe docs_serve`.

<!-- slug: getting-started -->
## Getting Started

Python 3.11+ is the only prerequisite; `bin/venv.sh` installs [Poetry](https://python-poetry.org/) when it is missing.

<!-- slug: install -->
### Install

#### As a dependency

```bash
pip install pure-schema-regimes
poetry add pure-schema-regimes
```

#### For development

```bash
git clone https://github.com/guilhermegor/pure-schema-regimes.git
cd pure-schema-regimes
bash bin/venv.sh
poetry run poe init
```

`poe` lives inside the virtualenv, so `bin/venv.sh` creates it first; `poetry run poe init` then
runs it without activating anything. If `poetry` is not on `PATH` (for example right after
`bin/venv.sh` installed it with `--user`), use `bash bin/poe_exec.sh init`, which finds the
venv's `poe` on its own. Behind a TLS-inspecting proxy with `bin/corporate_ca.pem` in place, run
`init` through `bash bin/poe_exec.sh init` so the CA bundle is wired for the downloads.

<!-- slug: usage -->
### Usage

```python
from pure_schema_regimes import RegimeRegistry, RegimeWindow

cls_registry = RegimeRegistry(
    [
        RegimeWindow("cnpj_keyed", int_period_start=None, int_period_end=202311),
        RegimeWindow("cnpj_classe_keyed", int_period_start=202312, int_period_end=None),
    ]
)

cls_registry.resolve(202312).str_name  # "cnpj_classe_keyed"
```

More recipes, including `RegimeBoundAdapter` and `SpecGapRegistry`, are in the
[examples](https://guilhermegor.github.io/pure-schema-regimes/examples/).

<!-- slug: project-structure -->
## Project Structure

```text
pure-schema-regimes/
├── .github/        workflows, CODEOWNERS, PR template
├── .specs/         feature specs and backlog trackers
├── bin/            gate scripts and helpers
├── docs/           published documentation
├── src/            application code
├── tests/
│   ├── unit/
│   └── integration/
├── pyproject.toml
└── poe_tasks.toml  task runner entry points
```

<!-- slug: development -->
## Development

After the bootstrap under Install, any task can be run with
`poetry run poe <task>`, and `poetry run poe` with no task lists them.

```bash
poetry run poe unit_tests
poetry run poe integration_tests
```

Once the first release's docs deploy has created the `gh-pages` branch, run
`poetry run poe enable_pages` once: until that branch exists, `init` leaves Pages untouched.

### `poetry run poe` or `bash bin/poe_exec.sh`?

Both run the same task through the same venv `poe`. Use `poetry run poe`, the command the
community knows best; `bin/poe_exec.sh` covers the cases where it is not enough:

| Case | `poetry run poe` | `bash bin/poe_exec.sh` |
|---|---|---|
| Normal machine, `poetry` on `PATH` | works | works |
| `poetry` not on `PATH` (e.g. right after `bin/venv.sh` installed it with `--user`) | fails: `poetry: command not found` | works: finds `.venv/bin/poe` (`.venv/Scripts/poe.exe` on Windows) without `poetry` |
| Corporate TLS-inspecting network, with `bin/corporate_ca.pem` present | gets no CA bundle; tasks that download can fail TLS | works: builds a union CA bundle and exports `REQUESTS_CA_BUNDLE`, `SSL_CERT_FILE`, `CURL_CA_BUNDLE` and `PIP_CERT` before the task runs |
| `poe` not installed | generic Poetry error | prints the install routes (`bin/venv.sh`, `pipx`, Poetry plugin) |

<!-- slug: public-api -->
## Public API

`RegimeWindow`, `RegimeRegistry`, `RegimeBoundAdapter` and `SpecGapRegistry`, imported from
`pure_schema_regimes`, plus `__version__`. That is the whole `__all__`; everything under
`_internal/` is private.

**1.x API guarantee.** From 1.0.0 on, this package follows [semantic versioning](https://semver.org/).
Every name in `__all__`, and the documented signatures and behaviour of its classes, stay
backward compatible across all 1.x releases: a 1.x upgrade never removes or renames a public
name or keyword argument, and never narrows what a call is documented to accept. A breaking
change ships only
in 2.0.0. As in semver, a bug fix is not a breaking change: when the code contradicts its
documented contract (for example, it accepts input the docs say it refuses), a 1.x PATCH
release corrects the code to match the docs. Anything under `_internal/` carries no guarantee
and can change in any release.

<!-- slug: publishing -->
## Publishing

Releases go out from the release workflows under `.github/workflows/`; the git tag is the
version.

The path from 0.x to 1.0.0, and the release gate that guards it, is in
[docs/releasing-1-0-0.md](docs/releasing-1-0-0.md).

<!-- slug: contributing -->
## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the branch, commit and review rules.

<!-- slug: license -->
## License

This project is licensed under MIT; see [LICENSE](LICENSE).

<!-- slug: authors -->
## Authors

- guilhermegor — [GitHub](https://github.com/guilhermegor) | [LinkedIn](https://www.linkedin.com/in/guilhermegor/)

<!-- slug: useful-links -->
## Useful Links

- [GitHub Repository](https://github.com/guilhermegor/pure-schema-regimes)
- [Issue Tracker](https://github.com/guilhermegor/pure-schema-regimes/issues)
- [Documentation](https://guilhermegor.github.io/pure-schema-regimes/)

---

<sub>Generated from the lib-minimal template via [BlueprintX](https://github.com/guilhermegor/blueprintx).</sub>
<!-- add any project disclaimer inside the sub tag above; for a library wrapping a third party, e.g. "Unofficial, community library. Not affiliated with or endorsed by ORG_NAME." -->
