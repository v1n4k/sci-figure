# Asset Strategy — drawio vs. external plotting libraries

## Two non-negotiable rules

### 1. Data, not layout

A library only earns a place in the asset stack if it produces **data**
(synthetic samples, dim-reduced coordinates, statistical structure,
density estimates) that drawio cannot fabricate.

Libraries whose primary role is **box-and-arrow layout** (`networkx`,
`graphviz`) overlap drawio and are explicitly *not* recommended —
drawio handles every layout case in this workflow with better pixel
control, semantic colour, and post-hoc tweakability.

Revisit graph libraries only if a future figure must display a *real*
graph dataset (citation network, learned attention graph, auto-generated
dependency tree) where the graph IS the data.

### 2. Cheap at one-shot runtime

The asset script runs end-to-end every time you iterate. A library is
acceptable if its **cold import is under ~500 ms** and **per-call cost
stays under ~2 s** for the asset sizes we render (typically 1600 × 1000 px
@ 200 dpi — kept under 2000 px on the longest side so multi-image agent
review doesn't hit the API's many-image dimension cap).

Libraries with JIT compile or subprocess-per-render overhead (numba,
headless Chromium) only earn their slot when nothing else can produce
the needed visualization.

## Tiered library list

### Default install (in `requirements.txt`)

| Library | Role | Runtime |
|---|---|---|
| `matplotlib` | Foundation; every other layer renders through it | Cold ~250 ms |
| `numpy` | Numerics | Cold ~150 ms |
| `Pillow` | Image I/O | Cold ~50 ms |
| `cairocffi` + `CairoSVG` | SVG → PNG conversion | Cold ~150 ms |

### Tier 1 — install on bootstrap (broadly useful)

All cheap at runtime; all "data, not layout".

| Library | What data it produces | Runtime |
|---|---|---|
| `scipy` | KDE bandwidths, Voronoi tessellations, interpolation grids, distributions | Cold ~300 ms; per-call μs–ms |
| `scikit-learn` | `make_blobs` / `make_moons` for honest synthetic clusters; `PCA` / `TSNE` (x, y) coordinates | Cold ~600 ms; `make_blobs` ~1 ms; **`TSNE` 1–10 s — cache** |
| `seaborn` | KDE / jointplot / heatmap / violin with sane defaults | Cold ~250 ms; per-plot matplotlib speed |

### Tier 2 — install only when a specific figure calls for it

| Library | Trigger | Runtime caveat |
|---|---|---|
| `umap-learn` | UMAP coords when t-SNE / PCA aren't enough | **Heavy: pulls `numba`, first-call JIT 10–30 s.** Worth it only if UMAP runs multiple times per script, or cache via `joblib.Memory`. |
| `adjustText` | Scatter / label de-collision when many class labels overlap | Cheap (~50 ms cold, 100–500 ms per call) |

### Tier 3 — narrow / heavy

| Library | Trade-off | Runtime caveat |
|---|---|---|
| `plotly` + `kaleido` | Only path to 3D scatter / interactive-then-static | **Each static export spawns headless Chromium (~1–3 s per PNG).** Use only for genuinely 3D content. |

### Explicitly NOT recommended

| Library | Why excluded |
|---|---|
| `networkx`, `graphviz` | Box-and-arrow layout is drawio's job. Adopt only if the graph is real data. |
| `scienceplots` | Imposes IEEE / Nature style sheets that conflict with custom semantic typography. |
| `bokeh`, `altair` | Rarely seen in NeurIPS / ICML / ICLR static figures. |
| `datashader` | Designed for million-point scatter; illustrative figures have ≤ a few hundred points. |

## Honesty rule

If the figure shows synthetic clusters, generate them with
`sklearn.datasets.make_blobs` rather than typing random offsets — the
result is reproducible and honest about what is a demonstration vs. a
real measurement.

## Runtime patterns for fast iteration

The asset script runs end-to-end every iteration; keep it under
~10 s wall-clock so you can rebuild fluently.

### Lazy-import heavy libraries inside the helpers that use them

```python
def feature_space_via_umap(path):
    import umap  # ~1.5 s — pay only when this helper actually runs
    reducer = umap.UMAP(...)
```

### Cache expensive renders to disk

```python
from joblib import Memory
cache = Memory(".cache/asset", verbose=0)

@cache.cache
def expensive_render(seed, scale, kind):
    ...
```

### Keep matplotlib in `Agg` backend

```python
import matplotlib
matplotlib.use("Agg")   # at the top of the script, before plt import
```

### Render in parallel for many independent assets

A `concurrent.futures.ProcessPoolExecutor` over per-helper closures
cuts a 10-asset build from ~10 s to ~3 s on a 4-core Mac. Don't
bother for ≤ 5 assets.

### Profile before optimising

A typical conference build's wall-clock decomposes as:
- Python imports (~1 s)
- matplotlib asset render (~3–5 s for ~10 PNGs)
- drawio CLI export (~10–15 s)

The drawio CLI export is the dominant cost. Library swaps inside the
asset stage recoup at most a few seconds — keep matplotlib unless you
need data geometry it can't produce.

## Library-agnostic asset rules (apply to any plotting backend)

- 200 dpi output, transparent background. Keep `figsize × dpi` so the
  longest side stays ≤ 2000 px; otherwise multi-image agent review trips
  the API's many-image dimension cap.
  - **Dense-detail escape hatch.** If an asset has dense small features
    (fine grid lines, small annotations, tight scatter clouds) that look
    aliased at 200 dpi when drawio scales it up, bump *that single
    asset* to `dpi=300` **and** drop `figsize` so the longest inch is
    ≤ 6.0 (→ ≤ 1800 px). Don't raise dpi without shrinking figsize —
    `8.0 × 300 = 2400 px` re-trips the cap. Keep the rest of the script
    at the 200 dpi default.
- Set in-asset typography floor globally at the top of the script
  (`apply_pub_rcparams()`); never lower per-helper.
- Strip axis chrome (`ax.set_axis_off()`) when the asset is purely
  illustrative — labels live as drawio TeX cells, not baked in.
- Use perceptually-uniform colormaps (`viridis`, `cividis`, `magma`)
  — never `jet`, never `rainbow`.
- Render once and inspect at 100 % zoom in Preview before embedding
  — PNGs are locked the moment they ship.

## Compose libraries freely

The tier list above is a recommendation of *what to install*, not a
prescription of *what each asset must use*. Within the constraints
("data, not layout" + "cheap at one-shot runtime"), combine
libraries however the figure's content calls for.

Small set of compositional examples (none mandatory):

| Asset | Combination |
|---|---|
| Honest synthetic feature space | `sklearn.datasets.make_blobs` for cluster centres + `sci_figure_lib.matplotlib_helpers.cluster_ellipsoid` for backdrop + matplotlib scatter for points |
| Density-shaded scatter | `seaborn.kdeplot(fill=True)` underlay + matplotlib scatter on top |
| Joint distribution panel | `seaborn.jointplot(kind="kde")` standalone, possibly with marginals |
| Per-class distribution strip | `seaborn.violinplot` or `seaborn.kdeplot` per class on shared axes |
| Manifold projection | `sklearn.manifold.TSNE` (cached via `joblib.Memory`) → matplotlib scatter with `apply_pub_scatter_style` |
| Confusion / similarity heatmap | `seaborn.heatmap(annot=False)` (no annotations — visual saturation carries magnitude) |
| Smoothed activation map | `numpy` Gaussian smoothing → `matplotlib.imshow(cmap='cividis')` |
| Smoothed score landscape | `scipy.ndimage.gaussian_filter` over a sampled grid → `matplotlib.contourf` |
| Decision boundary backdrop | `sklearn` classifier `predict_proba` over a mesh + `matplotlib.contourf` + scatter on top |
| Probability bar with hatched zero | matplotlib bar + `apply_pub_bar_style` + custom hatched empty bar |

Many other combinations are valid. The skill provides primitives
(`apply_pub_*_style`, `cluster_ellipsoid`); the figure's actual idiom
is yours to compose on top.

Evidence the combination is right:
- The 5-second skim test passes for the asset alone (open the PNG in
  Preview at 100 % — does the visual story land?).
- The asset has no leaked numerics / axis chrome / mechanics labels.
- The asset would still read at 25 % zoom (proxy for embed-and-print).
- The runtime is reasonable (≤ 2 s per asset, except the rare
  TSNE / UMAP cases which are cached).
