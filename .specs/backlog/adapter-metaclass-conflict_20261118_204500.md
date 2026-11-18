# Drop the metaclass from RegimeBoundAdapter's public base (#16)

Branch: `fix/16-adapter-metaclass-conflict`. PR #18.

## Done

- [x] `RegimeBoundAdapter` is a plain `ABC`, so a consumer subclass passing its own
      `ABCMeta`-derived `TypeChecker` no longer hits `TypeError: metaclass conflict`.
- [x] `__init__` carries `@type_checker`. The old metaclass skipped dunders, so the constructor
      was never actually checked before.
- [x] Added `tests/unit/test_regime_adapter_metaclass.py`: consumer-metaclass subclass builds,
      still refuses another regime's period, and a badly typed call raises `TypeError`.

## Completed — kept as a record

Every item is done and ships in PR #18, which closes #16.
