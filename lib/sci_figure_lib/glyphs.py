"""Reusable composed-cell glyphs for ML method figures.

Mixin pattern:

    class FigureBuilder(DrawioBuilder, GlyphMixin):
        ...

Every glyph takes either:
- a normalized fraction in [0, 1] for visual encoding (fill height /
  needle position), and / or
- explicit colours (no project palette baked in).

Semantic helpers such as ``distribution_bar_strip`` and ``readout_list``
are intentionally label-light. The per-figure script and requirements
log own whether a bar strip is evidence, an iterative posterior, or a
converged readout.

The labels α / β on ``gauge_glyph`` are conventional Greek for the
"two endpoints of a mixing dial" idiom — they are not project-specific.
Override via ``alpha_label`` / ``beta_label`` if you prefer different
glyphs.
"""

from __future__ import annotations

# Generic neutral colours used as defaults inside GlyphMixin. Project
# palettes override these via the explicit colour parameters.
_NEUTRAL_TRACK = "#E2E8F0"
_NEUTRAL_FRAME = "#CBD5E1"
_NEUTRAL_BG = "#FAFAFA"
_NEUTRAL_BG_SOFT = "#F8FAFC"
_NEUTRAL_NEEDLE = "#0F172A"


class GlyphMixin:
    """Domain glyphs that compose ``DrawioBuilder.cell()`` calls only.

    Used by mixing into a ``DrawioBuilder`` subclass:

        class MyBuilder(DrawioBuilder, GlyphMixin):
            ...
    """

    def distribution_bar_strip(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        labels: list[str],
        values: list[float],
        *,
        title: str | None = None,
        color: str = "#2563EB",
        track_color: str = _NEUTRAL_TRACK,
        fill: str = "#FFFFFF",
        stroke: str = _NEUTRAL_FRAME,
        prefix: str = "dist",
    ) -> str:
        """Compact horizontal bar distribution for evidence/posterior/readout.

        The caller's surrounding label must state the semantic level
        (evidence, iterative posterior, converged readout, etc.). This
        glyph only draws the reusable visual grammar.
        """

        if len(labels) != len(values):
            raise ValueError("labels and values must have the same length")
        if not labels:
            raise ValueError("at least one distribution row is required")

        bg = self.cell(
            "",
            x,
            y,
            w,
            h,
            f"rounded=1;arcSize=8;whiteSpace=wrap;html=1;"
            f"fillColor={fill};strokeColor={stroke};strokeWidth=1.1;",
            prefix=f"{prefix}_bg",
        )
        font = getattr(self, "font", "Helvetica")
        top_pad = 8
        if title:
            self.cell(
                title,
                x + 12,
                y + 6,
                w - 24,
                24,
                "text;html=1;strokeColor=none;fillColor=none;whiteSpace=wrap;"
                f"fontFamily={font};fontSize=18;fontColor={color};fontStyle=1;"
                "align=left;verticalAlign=middle;",
                prefix=f"{prefix}_title",
            )
            top_pad = 34
        pad_x = 12
        label_w = min(54, max(30, w * 0.16))
        row_gap = 6
        row_h = max(9, (h - top_pad - 8 - row_gap * (len(labels) - 1)) / len(labels))
        track_x = x + pad_x + label_w
        track_w = max(10, w - 2 * pad_x - label_w)
        for idx, (label, value) in enumerate(zip(labels, values)):
            yy = y + top_pad + idx * (row_h + row_gap)
            self.cell(
                label,
                x + pad_x,
                yy - 1,
                label_w - 6,
                row_h + 2,
                "text;html=1;strokeColor=none;fillColor=none;whiteSpace=wrap;"
                f"fontFamily={font};fontSize=16;fontColor=#64748B;fontStyle=1;"
                "align=left;verticalAlign=middle;",
                prefix=f"{prefix}_lab{idx}",
            )
            self.cell(
                "",
                track_x,
                yy,
                track_w,
                row_h,
                f"rounded=0;fillColor={track_color};strokeColor=none;",
                prefix=f"{prefix}_track{idx}",
            )
            frac = max(0.0, min(1.0, float(value)))
            self.cell(
                "",
                track_x,
                yy,
                max(2.0, track_w * frac),
                row_h,
                f"rounded=0;fillColor={color};strokeColor=none;",
                prefix=f"{prefix}_bar{idx}",
            )
        return bg

    def readout_list(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        header: str,
        items: list[str],
        *,
        color: str = "#7E22CE",
        fill: str = "#F5F3FF",
        prefix: str = "readout",
    ) -> str:
        """Final readout panel: one source with a clean list of uses."""

        if not items:
            raise ValueError("readout_list requires at least one item")
        bg = self.cell(
            "",
            x,
            y,
            w,
            h,
            f"rounded=1;arcSize=8;whiteSpace=wrap;html=1;"
            f"fillColor={fill};strokeColor={color};strokeWidth=1.5;",
            prefix=f"{prefix}_bg",
        )
        font = getattr(self, "font", "Helvetica")
        self.cell(
            header,
            x + 14,
            y + 10,
            w - 28,
            28,
            "text;html=1;strokeColor=none;fillColor=none;whiteSpace=wrap;"
            f"fontFamily={font};fontSize=20;fontColor={color};fontStyle=1;"
            "align=left;verticalAlign=middle;",
            prefix=f"{prefix}_header",
        )
        chip_h = max(28, min(42, (h - 54) / len(items) - 4))
        for idx, item in enumerate(items):
            yy = y + 48 + idx * (chip_h + 8)
            self.cell(
                item,
                x + 18,
                yy,
                w - 36,
                chip_h,
                "rounded=1;arcSize=8;whiteSpace=wrap;html=1;"
                f"fillColor=#FFFFFF;strokeColor={color};strokeWidth=1.2;"
                f"fontFamily={font};fontSize=18;fontColor={color};fontStyle=1;"
                "align=center;verticalAlign=middle;",
                prefix=f"{prefix}_item{idx}",
            )
        return bg

    def stacked_backplates(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        *,
        count: int = 3,
        offset: float = 8,
        fill: str = "#FFFFFF",
        stroke: str = "#93C5FD",
        prefix: str = "stack",
    ) -> str:
        """Draw backplates for genuinely multi-instance block-local objects."""

        if count < 1:
            raise ValueError("count must be at least 1")
        last = ""
        for idx in reversed(range(count)):
            op = 100 - idx * 18
            last = self.cell(
                "",
                x + idx * offset,
                y - idx * offset,
                w,
                h,
                f"rounded=1;arcSize=8;whiteSpace=wrap;html=1;"
                f"fillColor={fill};strokeColor={stroke};strokeWidth=1.2;opacity={max(35, op)};",
                prefix=f"{prefix}_{idx}",
            )
        return last

    def reliability_pill(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        top_frac: float,
        bot_frac: float,
        *,
        top_color: str = "#1D4ED8",
        bot_color: str = "#0891B2",
        prefix: str = "rely",
    ) -> str:
        """Two stacked horizontal fill-bars on a soft background.

        Encodes a *pair* of normalized magnitudes that visually combine —
        e.g. layer-quality + per-sample support, or any two reliability
        components. The reviewer reads "this is reliable iff both bars
        are full". Colours are caller-supplied so the glyph is
        domain-agnostic.
        """
        bg = self.cell(
            "",
            x,
            y,
            w,
            h,
            f"rounded=1;arcSize=14;whiteSpace=wrap;html=1;"
            f"fillColor={_NEUTRAL_BG_SOFT};strokeColor={_NEUTRAL_FRAME};strokeWidth=1.2;",
            prefix=f"{prefix}_bg",
        )
        pad = 6
        bar_h = (h - 3 * pad) / 2.0
        track_w = w - 2 * pad
        # Top bar
        self.cell(
            "", x + pad, y + pad, track_w, bar_h,
            f"rounded=0;fillColor={_NEUTRAL_TRACK};strokeColor=none;",
            prefix=f"{prefix}_t_track",
        )
        self.cell(
            "", x + pad, y + pad,
            max(2.0, track_w * float(top_frac)), bar_h,
            f"rounded=0;fillColor={top_color};strokeColor=none;",
            prefix=f"{prefix}_t_fill",
        )
        # Bottom bar
        bot_y = y + 2 * pad + bar_h
        self.cell(
            "", x + pad, bot_y, track_w, bar_h,
            f"rounded=0;fillColor={_NEUTRAL_TRACK};strokeColor=none;",
            prefix=f"{prefix}_b_track",
        )
        self.cell(
            "", x + pad, bot_y,
            max(2.0, track_w * float(bot_frac)), bar_h,
            f"rounded=0;fillColor={bot_color};strokeColor=none;",
            prefix=f"{prefix}_b_fill",
        )
        return bg

    def thermometer_glyph(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        fill_frac: float,
        color: str,
        *,
        prefix: str = "therm",
    ) -> str:
        """Vertical thermometer: outer pill + bottom-up colored fill.

        ``fill_frac`` ∈ [0, 1] is the visual height of the mercury column.
        """
        bg = self.cell(
            "", x, y, w, h,
            f"rounded=1;arcSize=40;whiteSpace=wrap;html=1;"
            f"fillColor=#FFFFFF;strokeColor={color};strokeWidth=2.0;",
            prefix=f"{prefix}_bg",
        )
        pad = 4
        inner_w = w - 2 * pad
        inner_h = h - 2 * pad
        fill_h = max(2.0, inner_h * float(fill_frac))
        self.cell(
            "", x + pad, y + pad + (inner_h - fill_h), inner_w, fill_h,
            f"rounded=1;arcSize=40;fillColor={color};strokeColor=none;",
            prefix=f"{prefix}_fill",
        )
        return bg

    def validity_meter(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        fill_frac: float,
        *,
        color: str = "#0891B2",
        prefix: str = "vmeter",
    ) -> str:
        """Horizontal pill: grey track + colored proportional fill from left.

        ``fill_frac`` ∈ [0, 1].
        """
        bg = self.cell(
            "", x, y, w, h,
            "rounded=1;arcSize=22;whiteSpace=wrap;html=1;"
            f"fillColor={_NEUTRAL_TRACK};strokeColor=#94A3B8;strokeWidth=1.2;",
            prefix=f"{prefix}_bg",
        )
        pad = 3
        fill_w = max(2.0, (w - 2 * pad) * float(fill_frac))
        self.cell(
            "", x + pad, y + pad, fill_w, h - 2 * pad,
            f"rounded=1;arcSize=22;fillColor={color};strokeColor=none;",
            prefix=f"{prefix}_fill",
        )
        return bg

    def gauge_glyph(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        needle_frac: float,
        *,
        left_color: str = "#1D4ED8",
        right_color: str = "#7E22CE",
        alpha_label: str = "&alpha;",
        beta_label: str = "&beta;",
        prefix: str = "gauge",
    ) -> str:
        """Horizontal mixing dial with a needle and α/β endpoint labels.

        Pale-tinted left and right halves; thin vertical needle at
        ``needle_frac`` ∈ [0, 1] indicates the mix. Endpoint labels can
        be overridden if the figure prefers different conventions.
        """
        # Background body
        bg = self.cell(
            "", x, y, w, h,
            f"rounded=1;arcSize=30;whiteSpace=wrap;html=1;"
            f"fillColor={_NEUTRAL_BG};strokeColor={_NEUTRAL_FRAME};strokeWidth=1.4;",
            prefix=f"{prefix}_bg",
        )
        pad = 4
        inner_w = w - 2 * pad
        inner_h = h - 2 * pad
        half_w = inner_w / 2.0
        # Pale left half
        self.cell(
            "", x + pad, y + pad, half_w, inner_h,
            f"rounded=0;fillColor=#DBEAFE;strokeColor=none;opacity=70;",
            prefix=f"{prefix}_lhalf",
        )
        # Pale right half
        self.cell(
            "", x + pad + half_w, y + pad, half_w, inner_h,
            f"rounded=0;fillColor=#F3E8FF;strokeColor=none;opacity=70;",
            prefix=f"{prefix}_rhalf",
        )
        # Needle: thin vertical bar at fractional x position
        nx = x + pad + inner_w * float(needle_frac) - 2.0
        self.cell(
            "", nx, y + pad - 4, 4, inner_h + 8,
            f"rounded=0;fillColor={_NEUTRAL_NEEDLE};strokeColor=none;",
            prefix=f"{prefix}_needle",
        )
        # Endpoint labels
        font = getattr(self, "font", "Helvetica")
        self.cell(
            alpha_label, x - 26, y, 24, h,
            "text;html=1;strokeColor=none;fillColor=none;whiteSpace=wrap;rounded=0;"
            f"fontFamily={font};fontSize=20;fontColor={left_color};fontStyle=1;"
            "align=right;verticalAlign=middle;",
            prefix=f"{prefix}_a",
        )
        self.cell(
            beta_label, x + w + 4, y, 24, h,
            "text;html=1;strokeColor=none;fillColor=none;whiteSpace=wrap;rounded=0;"
            f"fontFamily={font};fontSize=20;fontColor={right_color};fontStyle=1;"
            "align=left;verticalAlign=middle;",
            prefix=f"{prefix}_b",
        )
        return bg

    def model_glyph(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        *,
        color: str = "#1D4ED8",
        frozen: bool = False,
        prefix: str = "model",
    ) -> str:
        """Stacked-encoder glyph: 4 thin vertical layers under a rounded frame.

        If ``frozen=True`` a small snowflake (❄) glyph appears in the
        top-right corner (use for any "parameters not updated" model).
        """
        bg = self.cell(
            "", x, y, w, h,
            f"rounded=1;arcSize=12;whiteSpace=wrap;html=1;"
            f"fillColor=#FFFFFF;strokeColor={color};strokeWidth=2.0;",
            prefix=f"{prefix}_bg",
        )
        n = 4
        pad_x, pad_y = 10, 12
        gap = 6
        avail_w = w - 2 * pad_x - (n - 1) * gap
        layer_w = avail_w / n
        layer_h = h - 2 * pad_y
        opacities = [80, 65, 50, 35]
        for i in range(n):
            lx = x + pad_x + i * (layer_w + gap)
            self.cell(
                "", lx, y + pad_y, layer_w, layer_h,
                f"rounded=1;arcSize=18;fillColor={color};opacity={opacities[i]};"
                "strokeColor=none;",
                prefix=f"{prefix}_L{i}",
            )
        if frozen:
            font = getattr(self, "font", "Helvetica")
            self.cell(
                "&#10052;",  # snowflake
                x + w - 30, y + 4, 26, 22,
                "text;html=1;strokeColor=none;fillColor=none;whiteSpace=wrap;"
                f"fontFamily={font};fontSize=20;fontColor=#1D4ED8;"
                "align=center;verticalAlign=middle;",
                prefix=f"{prefix}_snow",
            )
        return bg

    def dataset_glyph(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        *,
        color: str = "#2563EB",
        prefix: str = "ds",
    ) -> str:
        """Three offset rounded cards giving a "set of samples" feel.

        Cards are drawn back-to-front with slight down-right offsets and
        increasing opacity (back cards are faintest).
        """
        cw = w * 0.84
        ch = h * 0.78
        slack_x = w - cw
        slack_y = h - ch
        # rel_x, rel_y, opacity
        offsets = [(0.0, 0.0, 38), (0.5, 0.5, 60), (1.0, 1.0, 100)]
        last = ""
        for i, (rx, ry, op) in enumerate(offsets):
            cx = x + slack_x * rx
            cy = y + slack_y * ry
            last = self.cell(
                "", cx, cy, cw, ch,
                f"rounded=1;arcSize=14;whiteSpace=wrap;html=1;"
                f"fillColor=#FFFFFF;strokeColor={color};strokeWidth=1.8;opacity={op};",
                prefix=f"{prefix}_c{i}",
            )
        return last
