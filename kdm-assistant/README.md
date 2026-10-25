# Lantern Archive app guide

The app implements KDM Rulemaster. Read the [roadmap](../docs/OBJECTIVE_AND_ROADMAP.md) and [current status](../docs/STATUS.md) for scope and next work. [Coverage](../docs/COVERAGE.md) lists reviewed topics and evidence. This guide owns operation.

## Run locally

Use Python 3.10 or newer. Double-click `Start.cmd` here, or run `python server.py --open`. Default address: [localhost:8765](http://127.0.0.1:8765). Local lookup requires no package installation, key, or internet connection.

Keep the server console open; Ctrl+C stops it. The launcher opens an existing service identifying itself as Lantern Archive without distinguishing checkouts. To run this worktree on another port, use `python server.py --port 8766 --open` here. Worktree identity checking remains a tracked follow-up.

Ask in the main view. Conversation history and Sources open in drawers. Rulebook citations open mapped pages; card citations open images. Answer settings controls optional explanations. Local history and pending corrections are stored in `data/history.sqlite3`, created on use. Closing the browser does not stop the server.

## Answer behavior

Local lookup returns reviewed references. Supported tables use code to choose outcomes. Follow-up parsing is bounded; use explicit table controls when needed. Roll inputs are final results including modifiers; the app does not determine modifier legality.

Lexical selection can find relevant evidence without establishing every part of a question. Missing-source, ambiguity, and edition boundaries remain necessary. Only the first Age milestone and severe Head table are reviewed. Other editions are unverified. Regression passes do not establish unrestricted accuracy.

## Branches and hosted access

Development continues on `rules-v2`; the user authorized promoting the reviewed work onto `main` on 24 October 2026. The integration preserves `main`'s shared-code access gate. Repository configuration disables automatic deployments for both branches. See [integration notes](../docs/MAIN_INTEGRATION.md) for scope, checks, and the distinction between a GitHub push and release readiness.

The Vercel project uses `kdm-assistant` as its root directory. Hosted access uses `KDM_ACCESS_CODE` and `KDM_SESSION_SECRET` to issue signed, secure 30-day browser sessions. The existing gate allows access when those settings are absent, so verify production configuration before any deployment. Rotate the session secret to end existing sessions. Secrets belong in server-side environment settings and must never be committed.

Hosted Sol remains disabled unless `KDM_ENABLE_SOL=true` is set. Keep it disabled until protection and the release checks pass. Local use retains SQLite history; hosted conversations and context stay in the player's browser. The hosted correction form is hidden because that deployment has no review database.

## Optional Sol explanations

GPT-6 Sol is opt-in per question through Answer settings. Eligible reference answers send the question and up to three reviewed records with low reasoning effort and a 700-token output cap. Supported exact tables and boundary responses stay local. Astra is excluded from normal and fallback app paths.

Keys may be `OPENAI_API_KEY` or `OPENAI_API_SECRET_KEY`. The code checks the worktree-root `.env`, then the app-folder `.env`, then environment variables. Here those paths are `D:\Documents\KDM\KDM-Rulemaster-v2\.env` and `D:\Documents\KDM\KDM-Rulemaster-v2\kdm-assistant\.env`. Keys are ignored by Git and are not browser assets. API billing is separate from ChatGPT/Codex billing.

Only selected reviewed content is supplied as evidence, including layout, linked-image availability, and interpretation limits. The model receives text metadata without image pixels. It directs players to available diagrams when exact square details are untranscribed. The app owns citations and instructs the model to omit page references from prose. Service failure retains the local reference. Fresh end-to-end explanation evaluation remains on the roadmap.

## Sources and regeneration

Images remain in `public/pages/` and `public/cards/`; mappings are in `data/manifest.json`. Startup computes current review flags and titles from records. PDFs and the page map are now under project-root `sources/`.

A missing local manifest invokes `prepare.py`, which reads `../sources/KDM_Rules_Focused_Page_Map.md`, reuses served images, and can render `../sources/KDM_Rulebook_1.5_Rules_Focused.pdf` through Poppler. Its optional `data/source-manifest.json` output is separate from current reviewed coverage.

Follow [the source workflow](../docs/SOURCES.md) for intake and preservation. Local original evidence and wiki drafts are ignored by Git. [Dormant wiki instructions](../docs/history/research/wiki/README.md) are archived; tools and tests remain here to preserve imports and commands.

## Verification

Run `python -m unittest discover -v` here. Tests cover records, selection, table boundaries, follow-ups, citations, persistence, HTTP/hosted handlers, and retained experimental tools. These are regression checks; [evaluations](../evaluation/INDEX.md) describe live and source-guided results and limits.

## Hosting, future release procedure

Automatic deployments are disabled for `rules-v2`; this branch is not cleared for hosting. Leave the separate `main` checkout untouched. Cleanup does not publish the app or alter access controls.

The existing deployment path uses `kdm-assistant` as Root Directory, static assets in `public/`, and stateless `api/index.py`. Hosted history/context stays in the browser; local SQLite remains local. The hosted correction form is hidden.

At the hosting phase, verify Vercel Authentication and named-friend access before enabling hosted Sol with `KDM_ENABLE_SOL=true`. Hosted Sol is disabled by default. Recheck configuration and the protected flow at that time. Historical deployment instructions and project comparisons remain in the [previous guide](../docs/history/handoffs/kdm-assistant-README-through-2026-10-24.md).
