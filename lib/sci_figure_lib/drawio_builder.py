"""DrawioBuilder — generic .drawio XML builder for conference figures.

Project-agnostic. Provides only the stable, generic API:
- ``cell``, ``image``, ``thumb_cell``, ``edge``, ``write`` (XML primitives)
- ``sub_panel`` (titled rounded-rect container with [A]/[B]/... tag)
- ``tex_cell`` (drawio MathJax with the ``\\(...\\)`` delimiters drawio
  actually accepts — see ``sci-figure/references/notation.md``)
- ``math_cell`` (HTML + Unicode escape hatch for figures that must avoid
  the MathJax dependency)
- ``stacked_frac`` (HTML span for inline vertical fractions inside math_cell)

Domain glyphs (model_glyph, dataset_glyph, reliability_pill, etc.) live in
``sci_figure_lib.glyphs.GlyphMixin``. Per-figure scripts subclass:

    class MyFigureBuilder(DrawioBuilder, GlyphMixin):
        ...
"""

from __future__ import annotations

import base64
from pathlib import Path
from xml.etree import ElementTree as ET

from PIL import Image

DEFAULT_FONT = "Helvetica"
DEFAULT_INK = "#1F2937"


def _b64(path: Path) -> str:
    """Return the base64 encoding of a file's bytes."""
    return base64.b64encode(Path(path).read_bytes()).decode("ascii")


class DrawioBuilder:
    """Generic .drawio XML builder.

    Parameters
    ----------
    assets:
        Mapping from asset key to PNG path; ``image()`` and ``thumb_cell()``
        look up source files here.
    page_w, page_h:
        Page dimensions in pixels.
    math:
        If True (default), set ``math="1"`` on ``mxGraphModel`` so drawio's
        MathJax renders ``$...$`` content in cells. Set False if you need
        every export path (CLI PNG / PDF / SVG) to display the raw text.
    diagram_name:
        Cosmetic name written into the ``diagram`` element.
    """

    DEFAULT_FONT: str = DEFAULT_FONT
    DEFAULT_INK: str = DEFAULT_INK

    def __init__(
        self,
        assets: dict[str, Path] | None = None,
        *,
        page_w: int = 3400,
        page_h: int = 1340,
        math: bool = True,
        diagram_name: str = "Figure",
        font: str | None = None,
    ) -> None:
        self.assets = assets or {}
        self.font = font or self.DEFAULT_FONT
        self.next_id = 2
        self.mxfile = ET.Element("mxfile", {"host": "draw.io", "type": "device"})
        diagram = ET.SubElement(
            self.mxfile, "diagram", {"name": diagram_name, "id": "figure"}
        )
        self.model = ET.SubElement(
            diagram,
            "mxGraphModel",
            {
                "dx": "1800",
                "dy": "900",
                "grid": "1",
                "gridSize": "10",
                "guides": "1",
                "tooltips": "1",
                "connect": "1",
                "arrows": "1",
                "fold": "1",
                "page": "1",
                "pageScale": "1",
                "pageWidth": str(page_w),
                "pageHeight": str(page_h),
                "math": "1" if math else "0",
                "shadow": "0",
            },
        )
        self.root = ET.SubElement(self.model, "root")
        ET.SubElement(self.root, "mxCell", {"id": "0"})
        ET.SubElement(self.root, "mxCell", {"id": "1", "parent": "0"})

    # ---------- low-level primitives ----------

    def _id(self, prefix: str = "cell") -> str:
        cid = f"{prefix}_{self.next_id}"
        self.next_id += 1
        return cid

    def cell(
        self,
        value: str,
        x: float,
        y: float,
        w: float,
        h: float,
        style: str,
        prefix: str = "node",
    ) -> str:
        """Add a generic mxCell. Returns the cell id (use as edge endpoints)."""
        cid = self._id(prefix)
        cell = ET.SubElement(
            self.root,
            "mxCell",
            {"id": cid, "value": value, "style": style, "vertex": "1", "parent": "1"},
        )
        ET.SubElement(
            cell,
            "mxGeometry",
            {"x": str(x), "y": str(y), "width": str(w), "height": str(h), "as": "geometry"},
        )
        return cid

    def image(
        self,
        key: str,
        x: float,
        y: float,
        w: float | None = None,
        h: float | None = None,
        prefix: str = "img",
    ) -> str:
        """Embed a PNG asset as a ``shape=image`` cell with strict aspect-ratio guard.

        Pass at most one of ``w`` / ``h`` and the missing dim is derived from
        the source PNG. If both are passed, they must match the source aspect
        within 0.5 % or this raises ``ValueError``.
        """
        src = Path(self.assets[key])
        sw, sh = Image.open(src).size
        if sw <= 0 or sh <= 0:
            raise ValueError(f"image({key}): source has invalid dims {sw}x{sh}")
        ar = sw / sh
        if w is None and h is None:
            raise ValueError(f"image({key}): pass at least one of w/h")
        if w is None:
            w = h * ar  # type: ignore[operator]
        elif h is None:
            h = w / ar
        else:
            cell_ar = w / h
            if abs(cell_ar - ar) / ar > 0.005:
                raise ValueError(
                    f"image({key}): geometry {w:g}x{h:g} (ar={cell_ar:.3f}) "
                    f"deviates from source {sw}x{sh} (ar={ar:.3f}) by "
                    f"{abs(cell_ar - ar) / ar * 100:.2f}% (>0.5% limit)"
                )
        data = _b64(src)
        style = (
            "shape=image;html=1;imageAspect=0;aspect=fixed;"
            "verticalLabelPosition=bottom;verticalAlign=top;"
            "strokeColor=none;fillColor=none;"
            f"image=data:image/png,{data};"
        )
        return self.cell("", x, y, w, h, style, prefix)

    def thumb_cell(
        self, key: str, x: float, y: float, side: float, prefix: str = "thumb"
    ) -> str:
        """Square-only thumbnail embed. Refuses non-square sources."""
        sw, sh = Image.open(Path(self.assets[key])).size
        if sw != sh:
            raise ValueError(
                f"thumb_cell({key}): source must be square, got {sw}x{sh}"
            )
        return self.image(key, x, y, side, side, prefix=prefix)

    # ---------- text + math cells ----------

    def math_cell(
        self,
        body_html: str,
        x: float,
        y: float,
        w: float,
        h: float,
        size: int = 22,
        color: str | None = None,
        align: str = "center",
        prefix: str = "eq",
    ) -> str:
        """HTML + Unicode math escape hatch (no MathJax).

        ``body_html`` may use ``<sub>``/``<sup>``, ``<b>``/``<i>``,
        Unicode symbols (μ, α, ∑, ∏, …), and the ``stacked_frac`` HTML
        helper for display fractions. Renders identically in the drawio
        app and every CLI export format **without** loading MathJax.

        Use this when the figure must not depend on MathJax (e.g.
        consistency with another tool, faster cold-render, simpler XML).
        For most figures, ``tex_cell`` produces nicer typography.
        """
        fc = color or self.DEFAULT_INK
        style = (
            "text;html=1;whiteSpace=wrap;strokeColor=none;fillColor=none;"
            f"align={align};verticalAlign=middle;"
            f"fontFamily={self.font};fontSize={size};fontColor={fc};"
        )
        return self.cell(body_html, x, y, w, h, style, prefix)

    def tex_cell(
        self,
        tex: str,
        x: float,
        y: float,
        w: float,
        h: float,
        *,
        size: int = 22,
        color: str | None = None,
        align: str = "center",
        display: bool = False,
        prefix: str = "tex",
    ) -> str:
        """LaTeX cell — drawio MathJax renders the math.

        Caller passes the raw LaTeX **without** delimiters; the helper
        wraps with the delimiter drawio's MathJax actually accepts:
        ``\\(...\\)`` for inline (default) or ``$$...$$`` for display
        mode (set ``display=True``).

        Note on delimiters: drawio's MathJax does **not** accept the
        single-dollar ``$...$`` form many MathJax setups use elsewhere.
        Only ``\\(...\\)``, ``$$...$$``, and AsciiMath backticks
        ``\\`...\\``` render. Using ``$...$`` produces literal text in
        both the app view and the CLI export.

        Both the drawio app and the CLI PNG / PDF export render math
        correctly with the right delimiters; SVG export does not.

        Requires ``math=True`` (the default) on the ``DrawioBuilder``.
        """
        fc = color or self.DEFAULT_INK
        body = f"$${tex}$$" if display else f"\\({tex}\\)"
        style = (
            "text;html=1;whiteSpace=wrap;strokeColor=none;fillColor=none;"
            f"align={align};verticalAlign=middle;"
            f"fontFamily={self.font};fontSize={size};fontColor={fc};"
        )
        return self.cell(body, x, y, w, h, style, prefix)

    def stacked_frac(
        self, num_html: str, den_html: str, color: str | None = None
    ) -> str:
        """HTML span rendering a vertical fraction with a horizontal bar.

        Use inside ``math_cell`` (HTML + Unicode) content when a stacked
        display fraction materially aids readability. Returns a string
        to embed. (For ``tex_cell``, just use LaTeX ``\\frac{...}{...}``.)
        """
        fc = color or self.DEFAULT_INK
        return (
            '<span style="display:inline-block;vertical-align:middle;'
            'text-align:center;line-height:1.0;padding:0 4px">'
            f'<span style="display:block;border-bottom:1.6px solid {fc};'
            'padding:0 2px 2px 2px">'
            f'{num_html}</span>'
            '<span style="display:block;padding:2px 2px 0 2px">'
            f'{den_html}</span>'
            '</span>'
        )

    # ---------- sub-panel container ([A] / [B] / ... layout) ----------

    def sub_panel(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        tag: str,
        title: str,
        *,
        fill: str = "#FBFCFD",
        stroke: str = "#CBD5E1",
        tag_color: str | None = None,
        title_color: str = "#475569",
        prefix: str = "sub",
    ) -> tuple[str, float, float, float, float]:
        """Titled sub-panel container (NeurIPS Fig. 1 norm).

        Renders a thin-stroked rounded rectangle with a 28-px header strip
        carrying a bold ``[A]`` tag and an italic title. Returns
        ``(panel_id, content_x, content_y, content_w, content_h)``.

        The title may contain inline LaTeX via ``\(...\)`` regions when
        ``math=True`` on the builder (the default).
        """
        tag_col = tag_color or self.DEFAULT_INK
        bg = self.cell(
            "",
            x,
            y,
            w,
            h,
            f"rounded=1;arcSize=5;whiteSpace=wrap;html=1;"
            f"fillColor={fill};strokeColor={stroke};strokeWidth=1.6;",
            prefix=f"{prefix}_bg",
        )
        tag_w = 56
        self.cell(
            tag,
            x + 12,
            y + 6,
            tag_w,
            26,
            "text;html=1;strokeColor=none;fillColor=none;whiteSpace=wrap;"
            f"fontFamily={self.font};fontSize=20;fontColor={tag_col};fontStyle=1;"
            "align=left;verticalAlign=middle;",
            prefix=f"{prefix}_tag",
        )
        self.cell(
            title,
            x + 14 + tag_w,
            y + 6,
            w - tag_w - 28,
            26,
            "text;html=1;strokeColor=none;fillColor=none;whiteSpace=wrap;"
            f"fontFamily={self.font};fontSize=22;fontColor={title_color};fontStyle=2;"
            "align=left;verticalAlign=middle;",
            prefix=f"{prefix}_title",
        )
        self.cell(
            "",
            x + 10,
            y + 34,
            w - 20,
            1,
            f"rounded=0;fillColor={stroke};strokeColor=none;",
            prefix=f"{prefix}_sep",
        )
        return bg, x + 12, y + 40, w - 24, h - 50

    # ---------- edges ----------

    def edge(
        self,
        source: str,
        target: str,
        value: str = "",
        color: str = "#334155",
        dashed: bool = False,
        prefix: str = "edge",
        stroke_width: int = 3,
        font_size: int = 22,
        exit_point: str | None = None,
        entry_point: str | None = None,
    ) -> str:
        """Add an orthogonal edge between two cell ids."""
        cid = self._id(prefix)
        dash = "dashed=1;dashPattern=8 6;" if dashed else ""
        ext = ""
        if exit_point:
            ex_x, ex_y = exit_point.split(",")
            ext += f"exitX={ex_x};exitY={ex_y};exitDx=0;exitDy=0;"
        if entry_point:
            en_x, en_y = entry_point.split(",")
            ext += f"entryX={en_x};entryY={en_y};entryDx=0;entryDy=0;"
        style = (
            "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;"
            "jettySize=auto;html=1;"
            f"endArrow=block;endFill=1;strokeWidth={stroke_width};"
            f"strokeColor={color};fontFamily={self.font};fontSize={font_size};"
            f"fontColor={color};{dash}{ext}"
        )
        edge = ET.SubElement(
            self.root,
            "mxCell",
            {
                "id": cid,
                "value": value,
                "style": style,
                "edge": "1",
                "parent": "1",
                "source": source,
                "target": target,
            },
        )
        ET.SubElement(edge, "mxGeometry", {"relative": "1", "as": "geometry"})
        return cid

    # ---------- emit ----------

    def write(self, path: Path) -> None:
        """Write the assembled .drawio XML to ``path``."""
        rough = ET.tostring(self.mxfile, encoding="unicode")
        pretty = '<?xml version="1.0" encoding="UTF-8"?>\n' + rough
        Path(path).write_text(pretty, encoding="utf-8")
