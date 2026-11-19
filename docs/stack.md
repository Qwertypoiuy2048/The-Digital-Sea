# Stack

| Area | Current choice | Grounded reason |
|---|---|---|
| Language | Python 3.13 verified locally | All application and test modules are Python; Python 3.13 runs the suite except for the known fixture assertion. |
| UI/runtime | Pygame `>=2.6.0` | Declared in `requirements.txt`; supplies windowing, drawing, and events. |
| Data | JSON + Python dictionaries | Four files under `data/`; no database dependency. |
| Tests | Python `unittest` | Both project test modules use it. |
| CI/procedure | GitHub Actions plus Azure YAML template | Workflow/pipeline and `scripts/ci-checks.sh` exist; branch protection status is UNKNOWN. |
| Packaging | pip + `requirements.txt` | Only dependency declaration present; no lockfile/package metadata. |
| Hosting/auth/database/queue/cache/monitoring/secrets | N/A | No implementation or dependency found. |

Pygame is load-bearing. Python 3.13 is verified locally; other supported versions, operating systems, exact license posture, and distribution method are UNKNOWN — needs human confirmation. Alternatives considered are not recorded and must not be invented.

## Update this document when

Update when requirements, Python support, runtime framework, storage, CI provider, packaging, hosting, or operations dependencies change.
