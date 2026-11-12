"""Export a trip guide page to CSV files you can import into Google My Maps.

Usage:
    python tools/export_mymaps.py okinawa-2026/index.html

Writes one CSV per island next to the page, in a "maps" folder, e.g.
    okinawa-2026/maps/ishigaki.csv
    okinawa-2026/maps/okinawa.csv

Each CSV becomes one map in Google My Maps (mymaps.google.com):
  Create a new map -> Import -> pick the CSV ->
  location column: "Search" -> title column: "Name" ->
  then "Uniform style" -> "Style by data column: Category" for colored pins.
"""
import csv
import json
import re
import sys
from urllib.parse import quote
from pathlib import Path

SECTIONS = {
    "food": "Restaurants & food",
    "kids": "Kids' activities",
    "play": "Playgrounds & amusement parks",
    "beach": "Beaches",
    "walk": "Walks & small hikes",
    "craft": "Arts & crafts",
    "shop": "Shopping & souvenirs",
    "mall": "Shopping malls & big stores",
    "used": "Secondhand & vintage",
    "local": "Local interest",
    "ww2": "World War II history",
    "more": "Anything else",
}


def load_data(html_path: Path) -> dict:
    """Pull the DATA object out of the page's script and parse it."""
    html = html_path.read_text(encoding="utf-8")
    m = re.search(r"const DATA=(\{.*?\n\}\});", html, re.S)
    if not m:
        sys.exit("Could not find 'const DATA=' in the page.")
    js = m.group(1)
    # The object uses bare keys (ishigaki:, areas:, food:...). Quote them so it is valid JSON.
    js = re.sub(r"(^|[{,\s])([a-z0-9]+):(?=[\[{])", r'\1"\2":', js)
    return json.loads(js)


def search_text(jp_name: str, jp_addr: str) -> str:
    """Same query the page's Maps button uses: Japanese name + address without the street number."""
    addr = re.sub(r"[0-9０-９\-]+$", "", jp_addr) if len(jp_addr) > 4 else jp_addr
    return f"{jp_name} {addr}".strip()


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    page = Path(sys.argv[1])
    out_dir = page.parent / "maps"
    out_dir.mkdir(exist_ok=True)
    data = load_data(page)

    for island, island_data in data.items():
        rows = []
        for key, label in SECTIONS.items():
            for item in island_data.get(key, []):
                area, en, jp, jp_addr, en_addr, note = item[:6]
                flag = item[6] if len(item) > 6 else ""
                query = search_text(jp, jp_addr)
                rows.append({
                    "Name": en,
                    "Japanese name": jp,
                    "Search": query,
                    "Category": label,
                    "Area": area,
                    "Address (JP)": jp_addr,
                    "Address (EN)": en_addr,
                    "Notes": f"{note} [{flag}]" if flag else note,
                    "Google Maps link": "https://www.google.com/maps/search/?api=1&query="
                    + quote(query),
                })
        out = out_dir / f"{island}.csv"
        # utf-8-sig so Excel also shows the Japanese correctly if you open the file.
        with out.open("w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print(f"{out}: {len(rows)} places")


if __name__ == "__main__":
    main()
