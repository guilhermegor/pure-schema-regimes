# Validate SpecGapRegistry entries on construction (#17)

Branch: `fix/17-spec-gap-registry-validation`. PR: #19.

## Done

- [x] `SpecGapRegistry.__init__` checks every entry. A key must be `str`, a value `frozenset`,
      and each element `str`. Anything else raises `TypeError` naming the key.
- [x] Refused `set` on purpose so the registry stays immutable after construction.
- [x] Added `tests/unit/test_spec_gap_registry.py`. Should-fail cases: `str`, `set` and `list`
      values, a non-`str` element, a non-`str` key, and a bad entry after a good one. Should-pass
      case: whole-name matching, where `CNPJ` must not match `CNPJ_FUNDO`.
- [x] Copied the mapping first and validated the copy, then stored it in a private
      `_dict_known_gaps`. `dict_known_gaps` is a read-only property that returns a
      `MappingProxyType` view, so the attribute cannot be rebound and the registry still
      pickles.
- [x] Added tests:
      - a write to the source dict after construction does not reach the registry;
      - the view refuses item assignment;
      - the property refuses rebinding;
      - pickle and deepcopy round-trip;
      - an empty `frozenset` is valid.
- [x] Made the `match=` assertions name messages only this module raises. They held in 30
      runs with varied hash seeds: `TypeChecker` skips dunders, so `__init__` is checked only
      by this module.

## Open

- [ ] Merge PR #19 after CodeRabbit review and green required checks.
