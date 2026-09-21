#!/usr/bin/env python3
"""
Generates manifest.json from the contents of the series/ folder.

Run this every time you add, rename, or remove photos.

Expected naming convention:

    series/<series-name>__<objective>/<value>um.<extension>

    <objective> must be one of: highmag, medmag, lowmag
    <value>     is the focus distance in µm (integer or decimal), e.g. 000, 025, 12.5

Example:

    series/copepod-01__medmag/000um.jpg
    series/copepod-01__medmag/025um.jpg
    series/copepod-01__medmag/050um.jpg
    series/diatom-03__highmag/000um.jpg
    series/diatom-03__highmag/025um.jpg

Usage:
    python3 generate_manifest.py
"""
import json
import os
import re

MAG_CODES = {
    "highmag": 0.53,   # High Mag.
    "medmag": 0.75,    # Med Mag.
    "lowmag": 1.34,    # Low Mag.
}

IMG_EXT = (".jpg", ".jpeg", ".png", ".webp")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SERIES_DIR = os.path.join(SCRIPT_DIR, "series")
MANIFEST_PATH = os.path.join(SCRIPT_DIR, "manifest.json")

FOLDER_RE = re.compile(r"^(.*)__(" + "|".join(MAG_CODES.keys()) + r")$")
FILE_RE = re.compile(r"^0*(\d+(?:\.\d+)?)\s*um", re.IGNORECASE)


def parse_folder(name):
    m = FOLDER_RE.match(name)
    if not m:
        return None
    slug, mag_code = m.groups()
    label = slug.replace("_", " ").replace("-", " ").strip()
    label = " ".join(w.capitalize() for w in label.split())
    return label, MAG_CODES[mag_code]


def parse_um(filename):
    m = FILE_RE.match(filename)
    return float(m.group(1)) if m else None


def main():
    if not os.path.isdir(SERIES_DIR):
        print(f"✗ Folder not found: {SERIES_DIR}")
        print("  Create a 'series/' folder next to this script.")
        return

    series = []
    for folder in sorted(os.listdir(SERIES_DIR)):
        full = os.path.join(SERIES_DIR, folder)
        if not os.path.isdir(full):
            continue

        parsed = parse_folder(folder)
        if not parsed:
            print(f"⚠ Skipped folder (invalid name, expected '...__highmag|medmag|lowmag'): {folder}")
            continue
        label, um_per_px = parsed

        images = []
        for fname in sorted(os.listdir(full)):
            if not fname.lower().endswith(IMG_EXT):
                continue
            um = parse_um(fname)
            if um is None:
                print(f"⚠ Skipped file (no µm value at the start of the name): {folder}/{fname}")
                continue
            images.append({"file": f"series/{folder}/{fname}", "um": um})

        images.sort(key=lambda x: x["um"])

        if len(images) < 2:
            print(f"⚠ Skipped series (fewer than 2 valid images): {folder}")
            continue

        series.append({"name": label, "umPerPx": um_per_px, "images": images})
        print(f"✔ {folder} → \"{label}\" ({um_per_px} µm/px, {len(images)} images)")

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(series, f, ensure_ascii=False, indent=2)

    print(f"\nmanifest.json generated with {len(series)} series → {MANIFEST_PATH}")


if __name__ == "__main__":
    main()
