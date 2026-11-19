# Testing

`tests/test_runtime.py` covers JSON shape, numeric/frequency helpers, derived resource totals, non-mutation, legacy inputs, validation errors, module/extension mutations, and resource rules. `tests/test_ui_and_layout.py` covers scaling, deterministic network positions, geometry, Pygame drawing at multiple sizes, coordinate conversion, selection/drag/zoom bounds, code scrolling, and screen routing.

UI tests set `SDL_VIDEODRIVER=dummy` before importing Pygame. No separate integration, contract, end-to-end, security, dependency-scan, or coverage tool/gate is configured. Fixture data is repository-local and contains no confirmed production data. Flaky tests are defects: reproduce, fix, or remove the invalid assertion with review evidence.

## Regression-safety check

For data/runtime changes, inspect `contracts.md` for every touched JSON key, public function, return field, error string, and invariant; add a focused test; then run both test modules. For UI/layout changes, run the UI suite and draw at the tested sizes. For playbook/CI changes, run the relevant `scripts/test/*.sh` fixture tests and `scripts/ci-checks.sh` where available. Record any baseline failure rather than treating it as a passing gate.

## Update this document when

Update when tests, runners, headless setup, coverage gates, fixtures, or CI test commands change.
