#!/usr/bin/env python3
"""Minimal SVG/PNG-stub chart renderer used by data-viz-charts fixture."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

PALETTES = {
    "corporate": ["#1f77b4", "#ff7f0e", "#2ca02c"],
    "okabe-ito": ["#0072B2", "#E69F00", "#009E73", "#CC79A7"],
}


def render_svg(data: list[dict[str, object]], title: str, palette_name: str) -> str:
    colors = PALETTES.get(palette_name, PALETTES["corporate"])
    max_val = max((float(row["value"]) for row in data), default=1.0) or 1.0
    bars = []
    for idx, row in enumerate(data):
        val = float(row["value"])
        label = str(row["label"])
        width = int((val / max_val) * 260)
        y = 40 + idx * 32
        color = colors[idx % len(colors)]
        bars.append(
            f'<text x="10" y="{y + 16}" font-size="12">{label}</text>'
            f'<rect x="110" y="{y}" width="{width}" height="20" fill="{color}" />'
            f'<text x="{118 + width}" y="{y + 16}" font-size="12">{val:g}</text>'
        )
    height = 60 + len(data) * 32
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="440" height="{height}">'
        f'<text x="10" y="22" font-size="15" font-weight="bold">{title}</text>'
        + "".join(bars)
        + "</svg>\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Render bar chart from JSON rows.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--title", default="Chart")
    parser.add_argument("--palette", default="corporate")
    args = parser.parse_args()

    rows = json.loads(args.input.read_text(encoding="utf-8"))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render_svg(rows, args.title, args.palette), encoding="utf-8")
    print(f"Wrote chart to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
