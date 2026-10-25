# Retrieval and table regression

See [the report](REPORT.md) for the final changes, verification, limits, and preservation checks. [Targeted decisions](CHECKS.md) and `checks.csv` compare the affected baseline cases with the final run.

- `final/`: final 16-scenario, 20-turn-per-mode HTTP rerun and metadata.
- Root `responses/`: initial development rerun, retained.
- `table-wording/`: deterministic follow-up after the Branding prose change, retained.
- `run.py`, `run_table_wording.py`, and `run_final.py`: saved run harnesses. They refuse to overwrite their result metadata or repeat a completed paid run.

The [original baseline](../2026-10-24-release-baseline/README.md) is unchanged. Its questions are now development/regression fixtures for these fixes. No independent release-accuracy claim is made. Read response records or CSV rows in targeted batches consistent with the user's data limits.
