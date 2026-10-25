# Rulebook sources

This folder preserves the original scan, the focused derivative, and their page mapping. Moving them did not change PDF content or page numbering.

- [Original scan](781787312-KDM-Rulebook-1-5.pdf)
- [Focused rulebook](KDM_Rulebook_1.5_Rules_Focused.pdf)
- [Page map](KDM_Rules_Focused_Page_Map.md)

The app serves existing page images from `kdm-assistant/public/pages/`. `prepare.py` now resolves the focused PDF and page map here. See [source review and preservation](../docs/SOURCES.md) for provenance, local image evidence, and intake rules. Both PDFs are above the user's file-read confirmation limit; this cleanup moved them without reading their contents.
