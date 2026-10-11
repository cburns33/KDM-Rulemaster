"""Stage one MediaWiki page for source review without adding it to app records."""

import argparse
import json
from pathlib import Path
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen


API_URL = "https://kingdomdeath.fandom.com/api.php"
OUTPUT_DIR = Path(__file__).parent / "data" / "wiki-candidates"
MAX_RESPONSE_BYTES = 15_000


def fetch_candidate(title, opener=urlopen):
    params = urlencode({
        "action": "query",
        "prop": "revisions",
        "rvprop": "ids|timestamp|content",
        "rvslots": "main",
        "format": "json",
        "formatversion": "2",
        "titles": title,
    })
    request = Request(
        f"{API_URL}?{params}",
        headers={"User-Agent": "KDM-Rulemaster/0.1 (private source review)"},
    )
    with opener(request, timeout=15) as response:
        payload = response.read(MAX_RESPONSE_BYTES + 1)
    if len(payload) > MAX_RESPONSE_BYTES:
        raise ValueError("Page response exceeds the 15 KB intake limit")

    pages = json.loads(payload)["query"]["pages"]
    if len(pages) != 1 or "missing" in pages[0]:
        raise ValueError(f"Expected one existing wiki page for {title!r}")
    page = pages[0]
    revision = page["revisions"][0]
    canonical_title = page["title"]
    return {
        "title": canonical_title,
        "page_id": page["pageid"],
        "revision_id": revision["revid"],
        "revision_timestamp": revision["timestamp"],
        "source_url": "https://kingdomdeath.fandom.com/wiki/"
        + quote(canonical_title.replace(" ", "_")),
        "edition_status": "unverified",
        "review_status": "unreviewed",
        "wikitext": revision["slots"]["main"]["content"],
    }


def save_candidate(candidate, output_dir=OUTPUT_DIR):
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{candidate['page_id']}-{candidate['revision_id']}.json"
    try:
        with path.open("x", encoding="utf-8") as output:
            json.dump(candidate, output, ensure_ascii=False, indent=2)
            output.write("\n")
    except FileExistsError:
        pass
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("title", help="Exact wiki page title; one page per run")
    args = parser.parse_args()
    path = save_candidate(fetch_candidate(args.title))
    print(f"Staged unreviewed source: {path}")


if __name__ == "__main__":
    main()
