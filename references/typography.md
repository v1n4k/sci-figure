# In-Asset Typography (matplotlib rcParams floor)

The asset PNGs are rendered at 300 dpi (typically 4000 × 2000 px) and
then **embedded** into the drawio canvas at much smaller on-canvas
size (e.g. 800 × 400 px). The downsample-to-embed cycle eats text
sharpness — anything that was 12 pt at render time becomes ~5 px on
the canvas after embed-and-downscale, which dies in the reviewer's
printout.

The lib provides `apply_pub_rcparams()` which sets the floor:

```python
plt.rcParams["font.size"]        = 26
plt.rcParams["axes.titlesize"]   = 36
plt.rcParams["axes.labelsize"]   = 32
plt.rcParams["xtick.labelsize"]  = 30
plt.rcParams["ytick.labelsize"]  = 30
plt.rcParams["legend.fontsize"]  = 30
plt.rcParams["figure.titlesize"] = 38
plt.rcParams["mathtext.fontset"] = "cm"   # match drawio MathJax
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["font.family"] = "DejaVu Sans"
```

## Rules

- **Call `apply_pub_rcparams()` once** at the top of
  `generate_assets.py`, after `matplotlib.use("Agg")`.
- **Only raise** these floors per-helper; never lower them.
  (Justification: a single helper that lowers below the floor
  produces a PNG that won't match the rest at conference scale.)
- **Bump `figsize` proportionally** so labels don't crowd. If a bar
  chart at default sizing feels cramped, increase `figsize` by ~20 %
  rather than shrinking the font.

## Match drawio MathJax

`mathtext.fontset = "cm"` makes matplotlib render `$\mu_x$` in
Computer Modern, which is also drawio MathJax's default. Mathmaticals
in matplotlib assets and drawio TeX cells will then look like the
same family.

## Asset-internal text

If the asset must carry baked text (a baked title, a per-bar class
label):

| Element | Floor (pt @ 300 dpi) |
|---|---|
| Tick label | 24 |
| Axis label | 28 |
| Legend entry | 26 |
| Title | 26 |

Anything below that becomes unreadable post-embed. Ideally, **strip
all asset-baked text** and let drawio cells provide the labels in the
final figure — that gives you a single typography pipeline (drawio
TeX) instead of two (matplotlib mathtext + drawio TeX).
