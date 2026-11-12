---
name: data-viz-charts
description: Generate publication-ready charts from tabular data with verified axis labels, units, and accessible palettes. Use when creating or updating data visualizations and report figures.
---

# Data Visualization Charts

Produce accurate, readable charts grounded in verified numeric columns and unit labels.

## Workflow

1. **Inspect source data:** Verify column names, units, and missing-value handling before plotting.
2. **Apply visual rules:** Follow the color, typography, and annotation standards in [references/palette-rules.md](references/palette-rules.md).
3. **Render with bundled helper:** Run `python scripts/render_chart.py --input data.json --out build/charts/out.png --palette corporate` to generate the chart artifact.
4. **Check legibility:** Confirm title, axis units, direct data labels, and non-overlapping ticks in the rendered output.
