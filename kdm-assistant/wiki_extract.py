"""Turn a locally staged wiki page into a readable, unreviewed card draft."""

import argparse
import html
import json
import re
from pathlib import Path


LINK = re.compile(r"\[\[([^]|]+)(?:\|([^]]+))?\]\]")
TEMPLATE = re.compile(r"\{\{([^{}]+)\}\}")
HEADING = re.compile(r"^(=+)\s*(.*?)\s*\1$")


def extract(candidate):
    source = candidate["wikitext"]
    categories = sorted(re.findall(r"\[\[Category:([^]]+)\]\]", source))
    match = re.search(r"^==\s*Card Text\s*==\s*$", source, re.M | re.I)
    if not match:
        raise ValueError("No Card Text heading found")
    source = source[match.end():].split("[[Category:", 1)[0]
    links = set()
    templates = set()

    def clean(value):
        value = LINK.sub(lambda m: links.add(m.group(1)) or (m.group(2) or m.group(1)), value)
        value = TEMPLATE.sub(lambda m: templates.add(m.group(1)) or f"[{m.group(1)} icon]", value)
        value = re.sub(r"<br\s*/?>", " / ", value, flags=re.I)
        value = re.sub(r"<[^>]+>", "", value)
        value = html.unescape(value.replace("'''", "").replace("''", ""))
        return " ".join(value.split())

    blocks = []
    table = None
    row = None
    for raw in source.splitlines():
        line = raw.strip()
        if not line:
            continue
        heading = HEADING.fullmatch(line)
        if heading:
            blocks.append({"type": "heading", "level": len(heading.group(1)),
                           "text": clean(heading.group(2))})
        elif line.startswith("{|", 0):
            table = {"type": "table", "rows": []}
            blocks.append(table)
            row = None
        elif line == "|}":
            table = None
            row = None
        elif table is not None and line == "|-":
            row = {"cells": []}
            table["rows"].append(row)
        elif table is not None and line.startswith(("!", "|")):
            if row is None:
                row = {"cells": []}
                table["rows"].append(row)
            kind = "header" if line.startswith("!") else "data"
            cell_source = line[1:].split("|", 1)[-1]
            cell = {"kind": kind, "text": clean(cell_source)}
            colspan = re.search(r'colspan=["\']?(\d+)', line)
            if colspan:
                cell["colspan"] = int(colspan.group(1))
            row["cells"].append(cell)
        elif table is not None and row and row["cells"]:
            row["cells"][-1]["text"] += " " + clean(line)
        elif line.startswith("*"):
            blocks.append({"type": "list_item", "text": clean(line.lstrip("* "))})
        else:
            text = clean(line)
            if text == "[Flow icon]":
                blocks.append({"type": "flow"})
            elif text:
                blocks.append({"type": "text", "text": text})

    return {
        "title": candidate["title"],
        "source_url": candidate["source_url"],
        "revision_id": candidate["revision_id"],
        "revision_timestamp": candidate["revision_timestamp"],
        "extraction_status": "draft",
        "review_status": "unreviewed",
        "categories": categories,
        "blocks": blocks,
        "linked_pages": sorted(links),
        "templates": sorted(templates),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path, help="Locally staged wiki JSON")
    args = parser.parse_args()
    candidate = json.loads(args.candidate.read_text(encoding="utf-8"))
    draft = extract(candidate)
    output = args.candidate.parent.parent / "wiki-drafts" / args.candidate.name
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8") as file:
        json.dump(draft, file, ensure_ascii=False, indent=2)
        file.write("\n")
    print(f"Drafted {draft['title']}: {len(draft['blocks'])} blocks, "
          f"{len(draft['linked_pages'])} linked pages, {len(draft['templates'])} templates")
    print(output)


if __name__ == "__main__":
    main()
