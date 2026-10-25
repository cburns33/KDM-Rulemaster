# KDM Rulemaster

A source-grounded assistant for the group's Kingdom Death: Monster 1.5 game. It should find applicable rulebook and card evidence, explain how it applies, show the sources, and identify missing coverage.

Start with the [objective, phases, and next steps](docs/OBJECTIVE_AND_ROADMAP.md), then the [current status](docs/STATUS.md). The roadmap owns the direction and release checkpoints; the status owns current counts, limits, and immediate work.

| Location | Purpose |
| --- | --- |
| [Objective and roadmap](docs/OBJECTIVE_AND_ROADMAP.md) | What completion means and the phases leading there |
| [First-release checklist](docs/RELEASE_CHECKLIST.md) | Required opening White Lion and early-campaign coverage, exclusions, and release gates |
| [Current status](docs/STATUS.md) | Present capabilities, limits, and next actions |
| [Coverage inventory](docs/COVERAGE.md) | Reviewed topics and their source evidence |
| [Source workflow](docs/SOURCES.md) | How evidence becomes coverage and what needs local preservation |
| [App guide](kdm-assistant/README.md) | Running the app, optional explanations, and checks |
| [Evaluation index](evaluation/INDEX.md) | Regression evidence and dated experiments |
| [History index](docs/history/README.md) | Superseded handoffs, paused research, and design previews |
| [Player introduction](docs/player/KDM_New_Player_Intro_and_Prologue_Reference.md) | First-session handout |

Development checkout: `D:\Documents\KDM\KDM-Rulemaster-v2`, branch `rules-v2`. The user authorized consolidating the reviewed work onto `main` on 24 October 2026 while preserving its shared-code access gate. Automatic deployments are disabled for both branches. A repository push does not establish hosted release readiness; the release checklist remains open.

The app and tests stay in `kdm-assistant/`. Original and focused PDFs and the page map are in `sources/`. App-served evidence stays in `kdm-assistant/public/`. Dated evaluation folders retain their depth so saved harnesses can locate the app and sibling results.
