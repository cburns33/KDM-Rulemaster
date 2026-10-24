# Rules assistant, iteration 2

This is the active development worktree for the source-grounded rules assistant. It is at `D:\Documents\KDM\KDM-Rulemaster-v2` on branch `rules-v2`, created from `main` commit `809a4f8` on 2 October 2026. Its rules and wiki-source work was committed as `1e3f1c4`. The separate `main` checkout at `D:\Documents\KDM\KDM-Rulemaster` contains the shared-code access gate and Grasp rule work in local commit `7027df5`. Local `main` has not been pushed. The Vercel production deployment uses `809a4f8`; pushing `main` can start a production deployment. The `rules-v2` Vercel config disables automatic deployments for this branch. This branch has not been cleared for hosting.

## Source update, 24 October 2026

The user supplied six photos from the group's physical 1.5 White Lion set. Maul and Combo Claw match the checked fields in their staged wiki drafts, and the photographed Grasp card defines the Grab term used by Maul. Claw and Size Up support earlier checks; Power Swat is a new photographed candidate. See `evaluation/2026-10-24-physical-white-lion-cards/REPORT.md`. Cunning's effect and a physical-set White Lion Data Card photo remain missing. The draft sources remain outside live answer retrieval. The older source-availability notes below record the state before these photos arrived.

## Mission

Build a rules assistant that can answer diverse, unseen Kingdom Death: Monster play questions from verified card and rulebook sources. It should find the relevant evidence, combine rules within their stated scope, show where the answer came from, and identify missing or conflicting evidence. Coverage should grow through reusable source records and retrieval behavior that transfer across questions.

Specific cases, including Enraged plus Grasp, are evaluation fixtures. They expose failure modes and verify improvements; they do not set the architecture. Before adding a special route or answer, ask which general rule, source relationship, or retrieval failure it represents. Test improvements against multiple phrasings, neighboring rules, and unsupported questions. Favor performance on held-out questions over fitting a known prompt.

Early-game play sets the order of source review. It does not narrow the design to White Lion or any one card. Asset filenames and duplicate images are catalog evidence; card text, edition, and playable deck composition require their own verification.

## Folder map

- `KDM_Project_Status.md`: current handoff at the top, followed by the older project history.
- `KDM_Early_Game_Card_Shortlist.md`: metadata-based candidates for later source checks. Its progression labels are provisional.
- `KDM_OCR_Queue.md`: first-pass scan, confirmed-skip, and hold decisions. It does not start OCR.
- `KDM_OCR_Benchmark_Selection.md`: seeded, metadata-only development and holdout candidates across six card families.
- `evaluation/2026-10-02-size-up-ocr/REPORT.md`: one-card OCR trial and image-checked corrections. This does not add a rule record.
- `evaluation/2026-10-02-claw-grasp-ocr/REPORT.md`: two more OCR trials, with profile-field omissions checked against the images.
- `evaluation/2026-10-02-enraged-grasp/REPORT.md`: the source audit for the first compound ruling.
- `kdm-assistant/`: the committed app baseline plus selected rules work from this iteration. `core_records.py` holds reviewed evidence, `engine.py` selects relevant records, and `test_*.py` checks behavior.
- `kdm-assistant/public/cards/white-lion-grasp.png`: a copy of the already extracted Grasp sample so the app can link to its card source.

The original sample comparison remains outside this repository at `D:\Documents\KDM\White Lion AI comparison`. The supplied rulebook PDFs and source-page library remain in their existing locations in this worktree. No further card extraction or OCR was carried over.

## Current scope

The app supports the level 1 Enraged plus Grasp ruling with a linked card image and rulebook pages. It can select up to two further reviewed records when a question spans topics. Local lookup presents those sources. The optional Sol path can use them to compose an answer, but it has not been live-tested for this iteration. The full Enraged card and higher-level cases remain unverified.

Wiki source intake now runs one exact page title at a time with `kdm-assistant/wiki_stage.py`. It saves the page URL, revision ID, timestamp, and original wikitext under the local, ignored `kdm-assistant/data/wiki-candidates/` folder, marked unreviewed with edition unverified. Maul, Combo Claw, and White Lion Data Card are staged, matching the three photographed 1.5 cards checked earlier. Staged pages do not enter answer retrieval or change the 18 reviewed records. Physical 1.5 remains the target; edition comparisons will be selective rather than a card-by-card gate. Wiki links, templates, and possible text omissions still need handling before a staged page can support a ruling.

The limited local extraction test converts those three staged revisions into unreviewed structured drafts without more wiki requests. See `evaluation/2026-10-05-wiki-extraction/REPORT.md`. The extractor preserves flow markers, table structure, linked terms, and template placeholders. The photographed White Lion data-card face confirms the level rows and Sniff; the wiki's additional Basic Action section has no supplied photo check. Drafts remain outside live answer retrieval.

The read-only Maul answer preview is in `evaluation/2026-10-07-maul-preview/REPORT.md`. It answers a card-text question from the existing draft, shows the wiki URL and revision, and flags the missing linked Grab definition. The draft remains outside reviewed 1.5 rulings. The preview establishes that this staged text can support a useful manually composed answer; automated answer composition remains untested. Bulk automated Fandom intake is paused while access and reuse permissions are unresolved under the current [Fandom terms](https://www.fandom.com/terms-of-use). The limited three-page extraction does not establish permission for a full pull.

The local `kdm-assistant/wiki_preview.py` command is an isolated model-backed draft-answer path. It takes one draft file or selects among the three local drafts, sends only the chosen draft's blocks to GPT-6 Sol, and appends provenance and requested missing linked-definition notices in code. The first bounded live test passed five distinct questions; see `evaluation/2026-10-07-wiki-preview/REPORT.md`. A fixed-question selection test passed nine source decisions, including two declines, and seven live draft answers; see `evaluation/2026-10-07-wiki-selection/REPORT.md`. The original checkout's key was used in memory because this worktree lacks its own key. The command is not connected to `/api/ask` or reviewed source records.

The same evaluation folder contains `SOURCE_AUDIT.md` and `combined-grab-preview.md`. A visual check of the available Grasp image and rulebook pages established Grab's effect in the Grasp context. The combined preview kept that evidence separate from the unreviewed Maul wiki text and declined a physical 1.5 Maul certification. The Maul, Combo Claw, and White Lion Data Card photos are not present as local files for a new edition check.

The October 7 [card-source search](evaluation/2026-10-07-wiki-selection/CARD_SOURCE_SEARCH.md) found Cunning listed in the focused 1.5 rulebook's White Lion level rows, but no definition there. A targeted official-site search did not yield the missing card faces or Cunning text. The next source check needs readable physical 1.5 images of Maul, Combo Claw, White Lion Data Card, and Cunning. These drafts remain unreviewed.

The access-gate work was not copied into this branch. Keep hosted Sol disabled and do not deploy this branch until hosting access is reviewed. The core Simulator bundle is encrypted, so additional image extraction remains blocked.

The Python test suite in `kdm-assistant` passes 81 tests. The next app-behavior evaluation is a held-out set of compound and unsupported questions across several topics. Use its results to judge retrieval, source selection, synthesis, citations, and abstention before choosing further architecture changes. The immediate wiki-path check is the separate Maul draft answer preview described above.
