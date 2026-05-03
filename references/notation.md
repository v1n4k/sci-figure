# Notation Policy

The skill renders math via drawio's built-in MathJax. Both the
drawio app and the CLI PNG / PDF export rasterize the math
correctly — there is no "open in app vs view in CLI" trade-off.

## Delimiters drawio actually accepts

This is the single most important thing to get right. Drawio's
MathJax is configured with non-standard delimiters:

| Form | Delimiter | Use |
|---|---|---|
| Inline LaTeX | `\(...\)` | default; embeds math in flowing text |
| Display LaTeX | `$$...$$` | larger, centred display equation |
| AsciiMath | `` `...` `` | shorter syntax for simple expressions |

**Drawio does NOT accept the single-dollar `$...$` form.** Cells
containing `$\mu_{\ell,c}$` render as the literal string
`$\mu_{\ell,c}$` in both the app view and any CLI export. This is
a common gotcha because most other MathJax setups (Jupyter, MkDocs,
Pandoc) accept `$...$` by default.

## Use the helpers — they wrap correctly

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

Before declaring a figure done, grep the produced `.drawio` source
for the broken-delimiter pattern:

```bash
grep -oE '\$[^$]+\$' artifacts/<figure>.drawio | head
```

Any non-empty output is a bug — those cells will render as literal
text. Fix by switching to `\(...\)` (or by removing the `$...$` if
the content was meant to be plain text).
