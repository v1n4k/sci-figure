# Notation Policy

The skill renders math via drawio's built-in MathJax. In practice,
math can render correctly in both the drawio app and the CLI PNG / PDF
export when cells use delimiters that drawio's MathJax accepts.

## Prefer helpers over hand-written delimiters

`tex_cell()` is the default path because it wraps raw LaTeX with the
delimiters this skill tests in drawio exports:

| Form | Delimiter | Use |
|---|---|---|
| Inline LaTeX | `\(...\)` | default; embeds math in flowing text |
| Display LaTeX | `$$...$$` | larger, centred display equation |
| AsciiMath | `` `...` `` | shorter syntax for simple expressions |

Bare `$...$` delimiters are less portable across drawio / export
configurations. If a hand-written cell uses them, verify the review PNG
before relying on it. If the delimiters render literally, switch that
cell to `tex_cell()` or `\(...\)`.

## Use the helpers — they wrap consistently

```python
from sci_figure_lib.drawio_builder import DrawioBuilder

d = DrawioBuilder({}, math=True)  # math=True is the default

# Inline (most common). Pass raw LaTeX without delimiters; the
# helper wraps with \(...\).
d.tex_cell(r"\mu_{\ell,c}", x, y, w, h, size=22, color="#1F2937")

# Display mode (centred, larger). Wraps with $$...$$.
d.tex_cell(r"q_x \propto t_x^{1-\beta_x} a_h^{\beta_x}",
           x, y, w, h, display=True, size=28)
```

For mixed inline math inside an HTML cell value, write the
delimiters yourself:

```python
d.cell(
    r'<i>blend \(t_x\) and \(a_h\) via \(\beta_x\)</i>',
    x, y, w, h, style_label,
)
```

## Symbol cheat sheet

| Concept | LaTeX |
|---|---|
| Scripted index | `\mu_{\ell,c}`, `t_x`, `a_h` |
| Loss / objective | `L_r`, `L_f`, `L_{\text{total}}` |
| Bold vector | `\mathbf{a}_h`, `\boldsymbol{\mu}_c` |
| Tilde | `\tilde P(x_f)` |
| Distribution / set | `D_r`, `D_f`, `\{\mu_{\ell,c}\}` |
| Norm / pipe | `\Vert`, `\|` |
| Greek mix dial endpoints | `\alpha`, `\beta` |

## When to use HTML + Unicode instead (`math_cell()`)

`tex_cell()` requires drawio to load MathJax (~ 200 KB JS) when the
file opens in the app, and adds a small render delay. For figures
with **no math at all**, you don't need MathJax — but for figures
with even one `\mu_{\ell,c}`, MathJax is loaded anyway, so you may
as well use it everywhere for consistency.

`math_cell(body_html, ...)` is the HTML + Unicode escape hatch:
`μ<sub>x</sub>`, `<b>α</b>`, `&beta;`. Plainer typography but no
MathJax dependency. Reserve for figures where MathJax must not be
loaded, or for inline text fragments where mixing `tex_cell()` would
require splitting the cell.

## Audit before shipping

Before declaring a figure done, inspect the review PNG and optionally
grep the produced `.drawio` source for hand-written `$...$` cells:

```bash
grep -oE '\$[^$]+\$' artifacts/<figure>.drawio | head
```

Non-empty output is not automatically a bug, but every match should be
visually checked. When in doubt, prefer `tex_cell()` so the generated
cell uses the skill's tested delimiters.
