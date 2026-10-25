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
FORBIDDEN_RE = re.compile(
    r"<\s*(?:animate|script|foreignObject|image|iframe)\b|@font-face|"
    r"(?:href|src)\s*=\s*[\"']https?:",
    re.I,
)


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
        if 'viewBox="0 0 640 480"' not in svg:
            raise SystemExit("bad viewBox for id %s" % scene_id)
        if FORBIDDEN_RE.search(svg):
            raise SystemExit("forbidden svg content for id %s" % scene_id)
        if len(svg) < 800:
            raise SystemExit("image too small for id %s (%s bytes)" % (scene_id, len(svg)))
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


# §1.5 multi-sense pairs. Both rows take zh_cue so the quiz can split near senses.
MULTI_SENSE_IDS = {
    6, 168, 9, 12, 13, 55, 14, 216, 15, 21, 20, 126, 24, 191, 32, 33,
    42, 43, 45, 46, 50, 153, 51, 52, 56, 57, 61, 62, 98, 99, 100, 101,
    114, 115, 123, 124, 130, 131, 199, 200, 217, 220,
}

# Concrete nouns and clear pictures that pass a glance without a gloss.
# Everything else is abstract, a functional verb, an odd gloss, or a multi-sense row.
CONCRETE_IDS = {
    2, 3, 4, 5, 7, 8, 18, 19, 25, 26, 27, 34, 37, 38, 39, 58, 64, 66, 67,
    69, 74, 75, 76, 78, 79, 80, 82, 84, 86, 87, 88, 89, 94, 95, 104, 109,
    112, 116, 118, 134, 135, 136, 137, 138, 141, 146, 147, 148, 149, 150,
    160, 162, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180,
    181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 193, 194, 196, 197,
    201, 203, 204, 205, 206, 209, 211, 213, 214, 215, 218,
}


def zh_cue_for(row):
    scene_id = int(row["id"])
    if scene_id in MULTI_SENSE_IDS:
        return True
    return scene_id not in CONCRETE_IDS


def write_bank(rows):
    lines = [
        "/** Picture vocab for 「看圖學英文」 v2.1. Independent of LOGIC_BANK and the daily pool.",
        " *  Gameplay answer is the English lemma only. zhCue asks the quiz to show zh as a hint.",
        " *  Images are original CC0 drawings; see assets/vocab/README.md.",
        " */",
        "window.VOCAB_PICTURE_BANK = [",
    ]
    for row in rows:
        scene_id = int(row["id"])
        image = "assets/vocab/images/w%03d.svg" % scene_id
        cue = "true" if zh_cue_for(row) else "false"
        lines.append(
            "  { id: %s, image: %s, answer: %s, altZh: %s, zh: %s, pos: %s, zhCue: %s },"
            % (
                js_string("w%03d" % scene_id),
                js_string(image),
                js_string(row["english"]),
                js_string(row["zh"]),
                js_string(row["zh"]),
                js_string(row["pos"]),
                cue,
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
    overlap = MULTI_SENSE_IDS & CONCRETE_IDS
    if overlap:
        raise SystemExit("multi-sense ids marked concrete: %s" % sorted(overlap))
    if len(MULTI_SENSE_IDS) != 42:
        raise SystemExit("expected 42 multi-sense ids, got %s" % len(MULTI_SENSE_IDS))
    hashes = render_all(rows)
    assert_distinct(rows, hashes)
    for row in rows:
        if int(row["id"]) in MULTI_SENSE_IDS and not zh_cue_for(row):
            raise SystemExit("multi-sense row missing zh_cue: %s" % row["id"])
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
