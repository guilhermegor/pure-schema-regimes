# Validate SpecGapRegistry entries on construction (#17)

Branch: `fix/17-spec-gap-registry-validation`. PR: #19.

## Done

- [x] `SpecGapRegistry.__init__` checks every entry. A key must be `str`, a value `frozenset`,
      and each element `str`. Anything else raises `TypeError` naming the key.
- [x] Refused `set` on purpose so the registry stays immutable after construction.
- [x] Added `tests/unit/test_spec_gap_registry.py`. Should-fail cases: `str`, `set` and `list`
      values, a non-`str` element, a non-`str` key, and a bad entry after a good one. Should-pass
      case: whole-name matching, where `CNPJ` must not match `CNPJ_FUNDO`.

## Open

- [ ] Merge PR #19 after CodeRabbit review and green required checks.
