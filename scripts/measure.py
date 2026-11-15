"""Score scan() against a labelled JSONL set (schema: rubrics/README.md).

    python3 -I scripts/measure.py eval/heldout2.jsonl [--out result.json] [--errors errors.jsonl]

A hit matches a label when the marker is the same and the spans overlap (labellers and
patterns may differ by an article or an object). Matching is one-to-one, in text order.

Reported per marker and language:
- span precision / recall, with include_defined=True and `invoked` ignored;
- default-mode precision / recall: scan() as a consumer calls it (invoked hits only)
  against the invoked labels;
- invoked and subtype accuracy over matched pairs.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from institutional_markers import MARKER_VERSIONS, MARKERS, PACKAGE_VERSION, scan  # noqa: E402


def label_span(text: str, quote: str, occurrence: int = 1) -> tuple[int, int]:
    pos = -1
    for _ in range(occurrence):
        pos = text.find(quote, pos + 1)
        if pos < 0:
            raise ValueError(f"quote {quote!r} (occurrence {occurrence}) not in {text!r}")
    return pos, pos + len(quote)


def match(hits, labels):
    """One-to-one overlap matching for one marker. Returns (pairs, unmatched_hits, unmatched_labels)."""
    pairs, used = [], set()
    free_hits = []
    for h in hits:
        for i, lab in enumerate(labels):
            if i not in used and h.start < lab["end"] and lab["start"] < h.end:
                pairs.append((h, lab))
                used.add(i)
                break
        else:
            free_hits.append(h)
    return pairs, free_hits, [lab for i, lab in enumerate(labels) if i not in used]


def ratio(a: int, b: int):
    return round(a / b, 3) if b else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--out")
    ap.add_argument("--errors")
    args = ap.parse_args()

    stats = defaultdict(lambda: defaultdict(int))
    errors = []
    records = [json.loads(line) for line in Path(args.path).read_text(encoding="utf-8").splitlines() if line.strip()]
    for rec in records:
        text, lang = rec["text"], rec["lang"]
        labels_by = defaultdict(list)
        for lab in rec["labels"]:
            s, e = label_span(text, lab["quote"], lab.get("occurrence", 1))
            labels_by[lab["marker"]].append({**lab, "start": s, "end": e})
        hits_by = defaultdict(list)
        for h in scan(text, lang=lang, include_defined=True):
            hits_by[h.marker].append(h)
        for marker in MARKERS:
            st = stats[(marker, lang)]
            hits, labels = hits_by[marker], labels_by[marker]
            pairs, fp, fn = match(hits, labels)
            st["hits"] += len(hits)
            st["labels"] += len(labels)
            st["tp"] += len(pairs)
            for h, lab in pairs:
                st["invoked_ok"] += h.invoked == lab["invoked"]
                if lab.get("subtype") is not None or MARKERS[marker].subtypes:
                    st["subtype_n"] += 1
                    st["subtype_ok"] += h.subtype == lab.get("subtype")
            # default mode: invoked hits vs invoked labels
            d_pairs, d_fp, d_fn = match([h for h in hits if h.invoked], [lab for lab in labels if lab["invoked"]])
            st["d_hits"] += len([h for h in hits if h.invoked])
            st["d_labels"] += len([lab for lab in labels if lab["invoked"]])
            st["d_tp"] += len(d_pairs)
            for h in fp:
                errors.append({"kind": "false_positive", "id": rec["id"], "marker": marker, "quote": h.quote,
                               "pattern": h.pattern_id, "invoked": h.invoked, "text": text})
            for lab in fn:
                errors.append({"kind": "missed", "id": rec["id"], "marker": marker, "quote": lab["quote"],
                               "invoked": lab["invoked"], "text": text})
            for h, lab in pairs:
                if h.invoked != lab["invoked"] or (MARKERS[marker].subtypes and h.subtype != lab.get("subtype")):
                    errors.append({"kind": "mismatch", "id": rec["id"], "marker": marker, "quote": h.quote,
                                   "label_quote": lab["quote"], "invoked": [h.invoked, lab["invoked"]],
                                   "subtype": [h.subtype, lab.get("subtype")], "text": text})

    rows = []
    for (marker, lang), st in sorted(stats.items()):
        rows.append({
            "marker": marker, "lang": lang, "version": MARKER_VERSIONS[marker],
            "hits": st["hits"], "labels": st["labels"], "matched": st["tp"],
            "precision": ratio(st["tp"], st["hits"]), "recall": ratio(st["tp"], st["labels"]),
            "default_precision": ratio(st["d_tp"], st["d_hits"]), "default_recall": ratio(st["d_tp"], st["d_labels"]),
            "invoked_accuracy": ratio(st["invoked_ok"], st["tp"]),
            "subtype_accuracy": ratio(st["subtype_ok"], st["subtype_n"]),
        })
    total = {k: sum(stats[x][k] for x in stats) for k in ("hits", "labels", "tp", "d_hits", "d_labels", "d_tp")}
    summary = {
        "package_version": PACKAGE_VERSION, "set": args.path, "records": len(records),
        "overall": {"precision": ratio(total["tp"], total["hits"]), "recall": ratio(total["tp"], total["labels"]),
                    "default_precision": ratio(total["d_tp"], total["d_hits"]),
                    "default_recall": ratio(total["d_tp"], total["d_labels"]), **total},
        "rows": rows,
    }

    print(f"{'marker':18} {'lang':4} {'hits':>4} {'lab':>4} {'P':>6} {'R':>6} {'P(def)':>7} {'R(def)':>7} {'inv':>6} {'sub':>6}")
    for r in rows:
        f = lambda v: "  -  " if v is None else f"{v:.2f}"  # noqa: E731
        print(f"{r['marker']:18} {r['lang']:4} {r['hits']:>4} {r['labels']:>4} {f(r['precision']):>6} {f(r['recall']):>6}"
              f" {f(r['default_precision']):>7} {f(r['default_recall']):>7} {f(r['invoked_accuracy']):>6} {f(r['subtype_accuracy']):>6}")
    o = summary["overall"]
    print(f"overall: P {o['precision']} R {o['recall']} | default P {o['default_precision']} R {o['default_recall']}"
          f" | {o['hits']} hits, {o['labels']} labels")
    if args.out:
        Path(args.out).write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.errors:
        Path(args.errors).write_text("\n".join(json.dumps(e, ensure_ascii=False) for e in errors) + "\n",
                                     encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
