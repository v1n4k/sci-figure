"""Small layout primitives for semantic figure composition.

The helpers in this module keep per-figure scripts at the "panel and
glyph" level. They do not know anything about drawio XML; they only
describe rectangles and simple splits that the drawio builder can render.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Rect:
    """Immutable rectangle in drawio canvas coordinates."""

    x: float
    y: float
    w: float
    h: float

    @property
    def right(self) -> float:
        return self.x + self.w

    @property
    def bottom(self) -> float:
        return self.y + self.h

    @property
    def cx(self) -> float:
        return self.x + self.w / 2.0

    @property
    def cy(self) -> float:
        return self.y + self.h / 2.0

    def inset(
        self,
        left: float = 0,
        top: float = 0,
        right: float = 0,
        bottom: float = 0,
    ) -> "Rect":
        """Return this rect reduced by side-specific padding."""

        return Rect(
            self.x + left,
            self.y + top,
            self.w - left - right,
            self.h - top - bottom,
        )

    def split_h(self, weights: Iterable[float], gap: float = 0) -> list["Rect"]:
        """Split left-to-right by proportional weights and fixed gaps."""

        ws = _normal_weights(weights)
        total_gap = gap * max(0, len(ws) - 1)
        usable = self.w - total_gap
        cur = self.x
        out: list[Rect] = []
        for weight in ws:
            width = usable * weight
            out.append(Rect(cur, self.y, width, self.h))
            cur += width + gap
        return out

    def split_v(self, weights: Iterable[float], gap: float = 0) -> list["Rect"]:
        """Split top-to-bottom by proportional weights and fixed gaps."""

        ws = _normal_weights(weights)
        total_gap = gap * max(0, len(ws) - 1)
        usable = self.h - total_gap
        cur = self.y
        out: list[Rect] = []
        for weight in ws:
            height = usable * weight
            out.append(Rect(self.x, cur, self.w, height))
            cur += height + gap
        return out

    def snap(self, grid: float = 10) -> "Rect":
        """Snap every coordinate and dimension to the nearest grid line."""

        if grid <= 0:
            raise ValueError("grid must be positive")
        return Rect(
            round(self.x / grid) * grid,
            round(self.y / grid) * grid,
            round(self.w / grid) * grid,
            round(self.h / grid) * grid,
        )


def union_rects(rects: Iterable[Rect]) -> Rect:
    """Return the bounding rectangle of one or more rectangles."""

    rs = list(rects)
    if not rs:
        raise ValueError("union_rects requires at least one Rect")
    left = min(r.x for r in rs)
    top = min(r.y for r in rs)
    right = max(r.right for r in rs)
    bottom = max(r.bottom for r in rs)
    return Rect(left, top, right - left, bottom - top)


def _normal_weights(weights: Iterable[float]) -> list[float]:
    ws = [float(w) for w in weights]
    if not ws:
        raise ValueError("at least one weight is required")
    if any(w <= 0 for w in ws):
        raise ValueError("weights must be positive")
    total = sum(ws)
    return [w / total for w in ws]
