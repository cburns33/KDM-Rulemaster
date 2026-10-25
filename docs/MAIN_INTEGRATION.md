# Main integration, 24 October 2026

The user authorized updating the project documents and pushing appropriate files to `main`. This supersedes the prior instruction to leave `main` untouched for this promotion. Continue routine rules/source development on `rules-v2` afterward.

## Included work

- Reviewed rule records, retrieval/table/follow-up repairs, diagram-source context, tests, and the source-linked runtime images already committed on `rules-v2`.
- Current objective, phases, first-release checklist, source/coverage inventories, navigation, and operation guide.
- Archived handoffs/research/design material and the original/focused PDFs under their organized paths. These are relocations of previously tracked material.
- Frozen baseline questions/results and separate regression/source-audit snapshots. Historical first responses and grades remain unchanged.
- The existing local `main` access gate and its documentation history, integrated with the newer rules work.

Credentials, local conversation databases, ignored source originals, wiki candidates/drafts, bytecode, and temporary files remain local. They are excluded from the commit. Ignored source evidence is preserved on disk.

## Hosting boundary

Repository configuration disables automatic deployments for both `main` and `rules-v2`. This GitHub update is not a production release. Current Vercel project settings could not be inspected because the connection returned a team-permission error. No hosting settings, environment variables, production domains, or deployed application were changed through the service.

The merged app retains the shared-code access gate. Hosted access depends on `KDM_ACCESS_CODE` and `KDM_SESSION_SECRET`; the existing implementation allows access when those settings are absent, so source inclusion alone does not establish a protected deployment. Hosted Sol still requires its explicit enablement setting. Do not publish or enable hosted Sol before checking production protection and the remaining release gates.

## Validation record

The integration combines rules checkpoint `1670bc1` with local `main` at `ced6c30`, including the access-gate commit `7027df5`. Merge conflicts were resolved in favor of the reviewed rules implementation while preserving the hosted API/access files and both access-session tests. Earlier `main` handoffs are preserved as [status](history/handoffs/main-status-before-2026-10-24-integration.md) and [app guide](history/handoffs/main-app-guide-before-2026-10-24-integration.md).

- All 128 Python tests pass on the combined `main` tree, including the two shared-access tests and the newer source/context checks.
- All 81 frozen baseline files retain aggregate SHA-256 `cb83fceb0887be0f9bf7a995fc071fa87653a81225b769330719cb31108e2e0d` in the staged rules checkpoint and the main checkout. Git attributes preserve saved evaluation bytes across checkout line endings.
- Both relocated PDFs and both prior main handoffs retain their original Git blob identities. Six access-gate files, including the hosted API, retain their pre-merge blobs.
- No credential, conversation database, bytecode, or ignored-data paths are staged. Historical source-guided answer checks and token totals remain in their original dated reports.
- The repository whitespace check passes. No paid evaluation was run for this documentation/Git consolidation.

This validated integration is the content authorized for `origin/main`. Routine development remains on `rules-v2`; a future production release still requires the open checklist gates.
