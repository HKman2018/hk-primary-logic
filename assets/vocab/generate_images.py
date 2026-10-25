"""Draw the v2 picture bank (original CC0 SVG) and refresh js/vocab-data.js.

From the repo root:

    python3 assets/vocab/generate_images.py

The site does not need this script at runtime. Images are original drawings,
not video frames.
"""

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from drawlib import Draw  # noqa: E402
from scenes_v2 import SCENES  # noqa: E402

WORDLIST = HERE / "wordlist-v2.json"
IMAGE_DIR = HERE / "images"
DATA_JS = ROOT / "js" / "vocab-data.js"
TEXT_RE = re.compile(r"<text\b[^>]*>(.*?)</text>", re.DOTALL)


def js_string(value):
    return json.dumps(value, ensure_ascii=False)


def render_all(rows):
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    written = {}
    for row in rows:
        scene_id = int(row["id"])
        if scene_id not in SCENES:
            raise SystemExit("missing scene for id %s" % scene_id)
        drawing = Draw()
        SCENES[scene_id](drawing)
        svg = drawing.svg()
        texts = [re.sub(r"\s+", " ", part).strip() for part in TEXT_RE.findall(svg)]
        blob = " ".join(texts).lower()
        answer = row["english"].strip().lower()
        if answer and answer in blob:
            raise SystemExit("answer %r leaked into image text for id %s" % (answer, scene_id))
        for part in texts:
            letters = re.findall(r"[A-Za-z]+", part)
            for word in letters:
                if word.upper() not in {"A", "B", "C", "P"}:
                    raise SystemExit("unexpected latin text %r in id %s" % (part, scene_id))
        if len(svg) < 200:
            raise SystemExit("image too small for id %s" % scene_id)
        name = "w%03d.svg" % scene_id
        target = IMAGE_DIR / name
        target.write_text(svg, encoding="utf-8")
        written[scene_id] = hashlib.sha256(svg.encode("utf-8")).hexdigest()
    return written


def assert_distinct(rows, hashes):
    seen = {}
    for row in rows:
        digest = hashes[int(row["id"])]
        previous = seen.get(digest)
        if previous is not None:
            raise SystemExit("identical image for id %s and %s" % (previous, row["id"]))
        seen[digest] = row["id"]
    by_english = {}
    for row in rows:
        by_english.setdefault(row["english"], []).append(row)
    for english, group in by_english.items():
        if len(group) < 2:
            continue
        hints = {item["image_hint"] for item in group}
        glosses = {item["zh"] for item in group}
        if len(hints) < len(group) or len(glosses) < len(group):
            raise SystemExit("multi-sense row collapsed for %s" % english)


def write_bank(rows):
    lines = [
        "/** Picture vocab for 「看圖學英文」 v2. Independent of LOGIC_BANK and the daily pool.",
        " *  Gameplay answer is the English lemma. zh and pos are kept for later use.",
        " *  Images are original CC0 drawings; see assets/vocab/README.md.",
        " */",
        "window.VOCAB_PICTURE_BANK = [",
    ]
    for row in rows:
        scene_id = int(row["id"])
        image = "assets/vocab/images/w%03d.svg" % scene_id
        lines.append(
            "  { id: %s, image: %s, answer: %s, altZh: %s, zh: %s, pos: %s },"
            % (
                js_string("w%03d" % scene_id),
                js_string(image),
                js_string(row["english"]),
                js_string(row["zh"]),
                js_string(row["zh"]),
                js_string(row["pos"]),
            )
        )
    lines.append("];")
    lines.append("")
    DATA_JS.write_text("\n".join(lines), encoding="utf-8")


def main():
    rows = json.loads(WORDLIST.read_text(encoding="utf-8"))
    if len(rows) != 222:
        raise SystemExit("expected 222 rows, got %s" % len(rows))
    if set(SCENES) != set(range(1, 223)):
        missing = sorted(set(range(1, 223)) - set(SCENES))
        extra = sorted(set(SCENES) - set(range(1, 223)))
        raise SystemExit("scene ids missing %s extra %s" % (missing, extra))
    hashes = render_all(rows)
    assert_distinct(rows, hashes)
    write_bank(rows)
    stale = [
        path.name
        for path in IMAGE_DIR.glob("*")
        if path.suffix == ".svg" and path.name not in {"w%03d.svg" % i for i in range(1, 223)}
    ]
    if stale:
        raise SystemExit("unexpected images: %s" % stale)
    print("wrote %s images and %s" % (len(hashes), DATA_JS.relative_to(ROOT)))


if __name__ == "__main__":
    main()
