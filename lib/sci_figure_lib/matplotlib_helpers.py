"""Matplotlib styling primitives — pure visual idioms, no story.

Three pieces:

1. ``apply_pub_rcparams()`` — sets the conference-typography floor on
   ``plt.rcParams`` globally. Call once at the top of an asset script.
   Only **raise** these floors per-helper; never lower them.

2. ``apply_pub_*_style(ax, ...)`` — axes-level decorators that apply
   the conference visual idiom (bar / scatter / fan) to an *existing*
   axes the caller built. The caller supplies the data, the title,
   and the palette — the lib never sees figure-specific story.

3. Convenience: ``cluster_ellipsoid(ax, center, scale, color)`` draws
   the nested-ellipsoid backdrop used in feature-space scatters.

These are project-agnostic. No class names, no notation, no values.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse


# ---------- 1. Global typography floor -----------------------------------

# Floor sizes (points) tuned so labels survive embed-and-downscale onto
# a ~3400 px conference canvas. Only raise per-helper; never lower.
_RCPARAMS_FLOOR: dict[str, object] = {
    "font.size": 26,
    "axes.titlesize": 36,
    "axes.labelsize": 32,
    "xtick.labelsize": 30,
    "ytick.labelsize": 30,
    "legend.fontsize": 30,
    "figure.titlesize": 38,
    "axes.unicode_minus": False,
    "mathtext.fontset": "cm",  # match drawio MathJax
    "font.family": "DejaVu Sans",
}


def apply_pub_rcparams() -> None:
    """Apply the publication-typography rcParams floor.

    Idempotent — call once at the top of an asset script. Matplotlib
    backend should already be ``Agg`` (set in headless asset scripts
    via ``matplotlib.use("Agg")``).
    """
    for k, v in _RCPARAMS_FLOOR.items():
        plt.rcParams[k] = v


# ---------- 2. Axes-level visual-idiom decorators ------------------------


def apply_pub_bar_style(ax, *, baseline: bool = True, baseline_color: str = "#94A3B8") -> None:
    """Apply the conference-bar-chart idiom to an existing axes.

    The caller has already drawn ``ax.bar(...)`` and may have set the
    title. This function:
    - removes y-axis tick labels (bar height carries magnitude),
    - adds a thin grey baseline at y=0 (optional),
    - hides top/right/bottom spines, leaves left spine subtle,
    - leaves the title and bar colours untouched.

    Pair with ``ax.bar(..., edgecolor='#0F172A', linewidth=2.0)`` for
    the matching ink-edge bar appearance.
    """
    ax.set_yticks([])
    if baseline:
        ax.axhline(0, color=baseline_color, lw=1.6, zorder=3)
    for spine in ("top", "right", "bottom"):
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color(baseline_color)
    ax.spines["left"].set_linewidth(1.4)


def apply_pub_scatter_style(ax) -> None:
    """Strip axis chrome for an illustrative scatter / feature-space plot.

    Use when the scatter's *position* and *colour* carry the message —
    axis numbers would just be visual noise. Pair with markers that
    have a white halo for visibility on tinted backgrounds.
    """
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect("equal")
    ax.set_axis_off()


def apply_pub_fan_style(ax) -> None:
    """Strip axis chrome for a fan / connection plot.

    Pair with ``ax.plot(..., solid_capstyle='round')`` and filled disk
    nodes (e.g. ``ax.scatter(..., marker='o', s=620, edgecolor='white',
    linewidth=3.0)``) for the rounded-ribbon idiom.
    """
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect("equal")
    ax.set_axis_off()


# ---------- 3. Cluster ellipsoid backdrop --------------------------------


def cluster_ellipsoid(
    ax,
    center,
    scale: float,
    color: str,
    *,
    angle: float = 0.0,
    levels: tuple[tuple[float, float], ...] = ((2.4, 0.05), (1.6, 0.10), (1.0, 0.16)),
    aspect_xy: tuple[float, float] = (4.0, 2.6),
) -> None:
    """Draw nested low-alpha ellipses behind a cluster scatter.

    Three concentric ellipses with decreasing radius and increasing alpha
    produce a soft "cloud → core" backdrop that reads as a cluster shape
    without saying so explicitly.

    Parameters
    ----------
    ax:
        Matplotlib axes.
    center:
        (x, y) cluster centre.
    scale:
        Scatter standard deviation; the ellipsoids' base radii are
        proportional to this.
    color:
        Cluster colour; ellipses use this with low alpha.
    angle:
        Rotation in degrees for visual variety across clusters.
    levels:
        Sequence of ``(radius_multiplier, alpha)`` pairs, drawn back-to-front.
    aspect_xy:
        (x_radius_factor, y_radius_factor) controlling ellipse shape.
    """
    fx, fy = aspect_xy
    for k, alpha in levels:
        ax.add_patch(
            Ellipse(
                xy=center,
                width=scale * fx * k,
                height=scale * fy * k,
                angle=angle,
                facecolor=color,
                alpha=alpha,
                edgecolor="none",
                zorder=1,
            )
        )
