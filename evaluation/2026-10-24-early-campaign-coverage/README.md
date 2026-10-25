# Early-campaign coverage artifacts

Start with [the source audit and results](REPORT.md). [Source hashes](source-hashes.tsv) identify reviewed evidence images.

Root response files preserve the first development snapshot. `final/` preserves the source-scope repair validation and is the current snapshot. Each JSON response contains the question and untouched returned payload. `checks.json` stores selection checks; `run-summary.json` stores execution, token, citation, and preservation totals. Read targeted records in accordance with the project's data-size rules.

`run.py` and `run_final.py` make paid requests and refuse an existing run's metadata. They are historical evaluation tools, not routine tests. Questions and expected selections are source-guided development fixtures. No independent release accuracy estimate is claimed.
