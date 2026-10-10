"""Scrape MileLion's card guide, diff against snapshot, print a Markdown report.

Exit code 0 = no changes, 1 = changes detected (also writes report to $GITHUB_OUTPUT).
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

URL = "https://milelion.com/credit-cards/guide/"
SNAPSHOT = Path(__file__).parent / "milelion_snapshot.json"


def normalize(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def scrape() -> dict:
    r = requests.get(URL, timeout=30, headers={"User-Agent": "miles-tracker/1.0"})
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    sections: dict[str, dict[str, dict]] = {}
    last_updated = ""

    # "Last update" banner
    m = re.search(r"Last update[^)]*?:\s*([^|)\n]+)", r.text)
    if m:
        last_updated = normalize(m.group(1))

    # Each h2 is a category; the next table lists cards
    for h2 in soup.find_all("h2"):
        title = normalize(h2.get_text(" ", strip=True))
        if not title or title.lower() in {"how can i find the mcc?", "discover more"}:
            continue
        # Find the card-listing table after this h2 (skip intro/"Main Article" tables).
        # Stop searching once we hit the next h2.
        table = None
        for el in h2.find_all_next(["h2", "table"]):
            if el.name == "h2":
                break
            header_cells = [normalize(td.get_text(" ", strip=True)) for td in el.find_all(["th", "td"])[:5]]
            if any("Earn Rate" in c or c == "Card" for c in header_cells):
                table = el
                break
        if not table:
            continue
        rows: dict[str, dict] = {}
        for tr in table.find_all("tr"):
            cells = [normalize(td.get_text(" ", strip=True)) for td in tr.find_all("td")]
            if len(cells) < 2:
                continue
            card = re.sub(r"\s+(Apply|Review|AMEX|Mastercard|Visa)$", "", cells[0]).strip()
            card = re.sub(r"\s+(Apply|Review)(\s+|$)", " ", card).strip()
            rate = cells[1]
            remarks = cells[2] if len(cells) >= 3 else ""
            if not card or not rate:
                continue
            rows[card] = {"rate": rate, "remarks": remarks}
        if rows:
            sections[title] = rows

    return {"last_updated": last_updated, "sections": sections}


def diff(old: dict, new: dict) -> list[str]:
    lines: list[str] = []
    if old.get("last_updated") != new.get("last_updated"):
        lines.append(
            f"**Guide `Last updated` changed:** `{old.get('last_updated', '(none)')}` → `{new.get('last_updated', '(none)')}`"
        )

    old_secs = old.get("sections", {})
    new_secs = new.get("sections", {})

    added_cats = sorted(set(new_secs) - set(old_secs))
    removed_cats = sorted(set(old_secs) - set(new_secs))
    if added_cats:
        lines.append(f"### New categories\n" + "\n".join(f"- {c}" for c in added_cats))
    if removed_cats:
        lines.append(f"### Removed categories\n" + "\n".join(f"- {c}" for c in removed_cats))

    for cat in sorted(set(old_secs) & set(new_secs)):
        o, n = old_secs[cat], new_secs[cat]
        added = sorted(set(n) - set(o))
        removed = sorted(set(o) - set(n))
        changed = [c for c in sorted(set(o) & set(n)) if o[c] != n[c]]
        if not (added or removed or changed):
            continue
        block = [f"### {cat}"]
        for c in added:
            block.append(f"- ➕ **{c}** — {n[c]['rate']} — {n[c]['remarks']}")
        for c in removed:
            block.append(f"- ➖ ~~{c}~~ (was {o[c]['rate']})")
        for c in changed:
            block.append(
                f"- ✏️ **{c}**: `{o[c]['rate']}` → `{n[c]['rate']}`"
                + (f" | remarks: `{o[c]['remarks']}` → `{n[c]['remarks']}`" if o[c]['remarks'] != n[c]['remarks'] else "")
            )
        lines.append("\n".join(block))

    return lines


def main() -> int:
    new = scrape()
    old = json.loads(SNAPSHOT.read_text()) if SNAPSHOT.exists() else {"last_updated": "", "sections": {}}

    report_lines = diff(old, new)
    changed = bool(report_lines)

    if changed:
        SNAPSHOT.write_text(json.dumps(new, indent=2, sort_keys=True) + "\n")
        report = "\n\n".join(report_lines)
    else:
        report = "No changes detected on MileLion guide."

    print(report)

    gh_output = os.environ.get("GITHUB_OUTPUT")
    if gh_output:
        with open(gh_output, "a") as fh:
            fh.write(f"changed={'true' if changed else 'false'}\n")
            fh.write("report<<MILELION_EOF\n")
            fh.write(report + "\n")
            fh.write("MILELION_EOF\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
