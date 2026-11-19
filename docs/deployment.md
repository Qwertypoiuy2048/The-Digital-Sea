# Deployment and operations

## Current state

The application is a local desktop prototype launched with Python from the repository. There is no installer, packaged release, hosting target, environment matrix, production deployment, monitoring, backup, secret manager, canary, feature-flag system, or rollback artifact. These are UNKNOWN — needs human confirmation if distribution is required.

GitHub Actions runs procedure/deck checks on pushes and pull requests; Azure DevOps contains a parallel pipeline template. Neither pipeline currently installs `requirements.txt` or runs the Python application tests. Whether either pipeline is connected and required by branch protection is UNKNOWN.

Local setup uses `sh scripts/setup-hooks.sh` where a POSIX shell is available. Hooks enforce task IDs, placeholder/secret checks, protected branches, and force-push protection. CI also runs shell/deck/task-ledger/procedure fixtures.

## Rollback

There is no deployed runtime to roll back. For local code, revert the reviewed commit or restore the prior checkout; for JSON, restore the prior tracked fixture. A real release process, artifact retention, rollback owner, and incident channel are UNKNOWN.

## Update this document when

Update when CI commands, supported platforms, packaging, release/deployment, feature flags, secrets, monitoring, or rollback procedures are added or changed.
