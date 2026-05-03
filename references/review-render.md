# Review-Render Sizing

The drawio CLI exports the figure as a high-DPI PNG (typically
~10 000 px on the longest side). That's too large for an agent
reviewer to read — Anthropic's image input has an effective ~2000 px
longest-side cap before files get "image too large" errors or are
heavily downscaled with quality loss.

But shrinking too far makes panel text and arrow labels unreadable.

## Hard bounds (enforced by `make_review_png`)

`sci_figure_lib.render.REVIEW_BOUNDS = (800, 1800)`.

| Bound | px (longest side) | Reason |
|---|---|---|
| Lower | 800 | Below this, sub-panel headers, arrow labels, and asset text become unreadable to either an agent or a human at 25 % zoom. |
| Upper | 1800 | Above this, an agent reviewer is at risk of "image too large" failures. |

`make_review_png(target_max_px=...)` raises `ValueError` outside
[800, 1800]. The default is 1500 — comfortable margin under the upper
cap, sharp enough that an agent can read every label.

## Render pipeline

```python
from sci_figure_lib.render import cli_export, make_review_png

OUT = ARTIFACT_DIR / "fig.drawio"
full_png = OUT.with_suffix(".drawio.png")              # ~10 000 px
cli_export(OUT, full_png)                              # CLI export
make_review_png(full_png, OUT.with_name("fig_review.png"),
                target_max_px=1500)                    # bounded
```

The full-resolution `<figure>.drawio.png` stays on disk for **human**
inspection at 100 % zoom. The reduced `<figure>_review.png` is the
artifact agents read.

## When to deviate from the default 1500

- **Agent-reviewer-only audit, dense figure:** stay at 1500. Below
  this you lose label legibility.
- **Single-panel crop for close inspection:** use
  `crop_review_png(src, dst, (x0, y0, x1, y1), target_max_px=1500)`
  to read one panel at higher effective resolution.
- **Quick sanity check, you'll open it yourself:** the full-resolution
  PNG is fine; skip `make_review_png`.

## Don't

- Do not bypass the bounds (`make_review_png` will raise).
- Do not call drawio CLI without `cli_export` — you'll skip the
  orphan-process cleanup.
- Do not commit the full-resolution PNG to source control if it's
  > 5 MB; commit the `.drawio` source instead.
