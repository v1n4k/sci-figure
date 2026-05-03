# Anti-patterns (do not regress)

## Building / iterating

- **Hand-editing the `.drawio` XML.** The script is the source of
  truth; manual edits get clobbered on the next regen. Edit the
  generator instead. (Tweaking individual cell positions in the drawio
  app for fine-tuning is fine — but don't add or rename cells there.)
- **Running both stages in one script** so a layout-only change
  re-renders every PNG. Keep `generate_assets.py` and
  `generate_figure.py` independent — that's the whole point of the
  two-script split.
- **Mixing matplotlib and drawio imports** in either script. Each
  imports only the libraries it actually uses.
- **Skipping `verify_aspect_ratios` before declaring a figure done.**
  An aspect-drift bug is invisible at small zoom and embarrassing at
  print scale.
- **Calling drawio CLI without `cli_export`.** You'll leak orphan
  Electron processes.

## Layout

- **Fattening a single panel to "say everything."** Split into
  sub-panels until each panel passes the 5-second skim test alone.
- **Forcing a uniform sub-panel grid** (every phase has 4 sub-panels)
  when the natural counts differ — produces dead space.
- **Sub-panels too close to touch.** ≥ 16 px gutters; arrows route
  through them.
- **Long arrows that cross unrelated cells.** Either route through
  a gutter or restructure the layout.

## Notation

- **Embedding equation rasters** (`eq*.png`) in the figure body. Use
  a drawio TeX cell or omit the equation. The lib's `tex_cell` is the
  one allowed entry point.
- **Naming an operator** (`softmax`, `normalize`, `cosine`) in a
  labelled box instead of showing what it produces. Replace the box
  with a glyph or a connecting arrow that lands on the operator's
  output.
- **Using single-dollar `$...$` MathJax delimiters.** Drawio's
  MathJax requires `\(...\)` (inline) or `$$...$$` (display); `$...$`
  produces literal text in both the app and the CLI export. Use
  `tex_cell()` from the lib (it wraps with the right delimiter) or
  write `\(...\)` directly inside HTML cell values.
- **Notation glossary inside the figure.** Defer notation explanation
  to the paper text or to inline panel captions.

## Asset rendering

- **Tiny labels** (< 24 pt) in matplotlib assets — they don't survive
  embed-and-downscale. See `typography.md`.
- **Baked-in axis chrome** (ticks, axis labels, panel titles) when
  drawio cells could carry the same labels with consistent typography.
  Strip with `apply_pub_scatter_style(ax)` etc.
- **`jet` / `rainbow` colormaps.** Use perceptually-uniform
  (`viridis`, `cividis`, `magma`).
- **Hand-tuned synthetic clusters** (literal `centers = [(-1.5, 0), …]`
  with random offsets) when `sklearn.datasets.make_blobs` gives
  honest, reproducible geometry.

## Palette

- **Reusing a colour for an unrelated concept** (blue used for both
  "retain" and "frozen" without semantic separation).
- **Using a class colour for a layout chrome element** (e.g. the
  same teal as a class for the sub-panel separator). Keep chrome in
  neutral greys.

## Scope creep — figure bloat

- **Trying to land everything in one figure.** This skill produces
  one figure per invocation. Don't try to fit the entire paper into
  it: every additional panel / glyph / arrow / label is a 5-second
  tax on the reviewer. Strip until the visual story is the *minimum
  sufficient* to land the figure's single message. Then stop. If the
  paper needs more visual content, that's a separate request — the
  user will say so explicitly.
- **Symptoms of bloat:** > 6 sub-elements in any one region; every
  region has its own caption explaining what's in it; the figure is
  described as "comprehensive" rather than focused.
- **Designing secondary / auxiliary figures unprompted.** If the
  user asked for "the main method figure", produce one figure. Don't
  speculate about Fig. 2, ablation plots, or supplementary diagrams
  unless the user opens that conversation themselves.
- **Re-explaining the figure in its caption.** If the figure can't
  stand alone visually, fix the figure, not the caption.

## File / folder structure

The skill expects this layout per project, with one figure per
`<name>` (anything matching `[A-Za-z0-9_-]+`):

```
project/
├── .venv/                                # bootstrapped once per project
├── scripts/
│   └── <name>/
│       ├── generate_assets.py            # matplotlib stage
│       ├── generate_figure.py            # drawio stage
│       └── Makefile                      # `make assets|figure|all|clean`
├── assets/
│   └── <name>/
│       └── *.png                         # asset PNGs only (300 dpi)
└── artifacts/
    ├── <name>.drawio                     # deliverable (editable source)
    └── <name>_review.png                 # deliverable (bounded review)
```

`new_figure.sh <name>` creates `scripts/<name>/`, `assets/<name>/`,
and `artifacts/` (if missing). `make clean` removes only that
figure's outputs.

**Folder hygiene rules:**

- **One figure = one `<name>` triple** (`scripts/<name>/`,
  `assets/<name>/`, `artifacts/<name>.*`). Never mix figures inside
  a single subdir — it tangles `make clean` and confuses the
  two-script independence guarantee.
- **Nothing in `assets/<name>/` other than the PNG outputs of
  `generate_assets.py`.** No notebooks, no debug renders, no
  `_old.png` backups. The contents of `assets/<name>/` is exactly
  the set of inputs `generate_figure.py` will read.
- **Nothing in `artifacts/` other than `<name>.drawio` and
  `<name>_review.png`** (per figure). The intermediate full-res
  `<name>.drawio.png` is deleted by `generate_figure.py` after the
  review PNG is produced; if you find one lingering, the script
  exited mid-run.
- **No hand-edited copies of generated files.** If you tweaked the
  rendered drawio in-app, fold the tweak back into
  `generate_figure.py` and regenerate. The script is the source of
  truth.
- **Cache directories are local-only.** `.venv/`, `__pycache__/`,
  `.cache/` (joblib), `*.egg-info/` — `.gitignore` them.
- **Don't dump shared utilities into `scripts/<name>/`.** If a helper
  is reusable across figures, it belongs in the skill's
  `lib/sci_figure_lib/`, not in a per-figure script. Per-figure
  scripts only own per-figure logic.

## Output management

- **Letting a debug crop or scratch PNG ship in `artifacts/`.**
  Rename and remove before committing.
- **Committing the full-resolution drawio CLI PNG** to the repo if
  it's > 5 MB. Commit the `.drawio` source plus the exported PDF.
- **Modifying `.agents/skills/drawio-skill/`** locally. That bundle
  tracks upstream; refresh via
  `bash .agents/skills/sci-figure/scripts/refresh_drawio_skill.sh`.
