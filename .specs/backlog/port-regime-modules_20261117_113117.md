# Port the regime adapter modules from blueprintx (#8)

Branch: `feat/8-port-regime-modules`.

## Done

- [x] Copied `regime_window`, `regime_registry`, `regime_adapter` and `spec_gap_registry` with
      their 18 tests from blueprintx `templates/python-common/src/utils/`.
- [x] Rewrote imports to `pure_schema_regimes.` and pointed the typing shim at
      `_internal.utils.typing`.
- [x] Added a stdlib `TypeChecker` metaclass so `bin/check_typing.py` holds in zero-dependency
      mode.
- [x] Removed the starter `main` and its test; exported the four classes from `__init__.py`.
- [x] Rewrote the README, `docs/usage.md`, `docs/examples.md`, `docs/api/reference.md` and
      `AGENTS.md` around the CVM fund-profile case.

## Open

- [x] Publish `0.1.0` to Test PyPI, verify the install, then publish to PyPI (needs the pending
      trusted publishers registered on both indexes). Released as
      https://github.com/guilhermegor/pure-schema-regimes/releases/tag/v0.1.0.
- [x] Report the zero-dependency `check_typing` gap upstream in blueprintx
      (guilhermegor/blueprintx#1204).

## Completed — kept as a record

Both open items are done: `0.1.0` is published and install-verified from a clean venv on
Test PyPI and PyPI, and the `check_typing` gap is filed upstream as
guilhermegor/blueprintx#1204.
