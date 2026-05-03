"""sci-figure-lib — generic infrastructure for conference-quality method figures.

Project-agnostic: the lib carries no class names, story values, or notation
symbols beyond conventional Greek (α, β). Every figure decision (colours,
classes, story values, titles) lives in the per-figure script.

Public API:
    from sci_figure_lib.drawio_builder import DrawioBuilder
    from sci_figure_lib.glyphs import GlyphMixin
    from sci_figure_lib.render import (
        verify_aspect_ratios, make_review_png, crop_review_png,
        cli_export, REVIEW_BOUNDS,
    )
    from sci_figure_lib.matplotlib_helpers import (
        apply_pub_rcparams, apply_pub_bar_style,
        apply_pub_scatter_style, apply_pub_fan_style,
    )
"""

from sci_figure_lib.drawio_builder import DrawioBuilder
from sci_figure_lib.glyphs import GlyphMixin
from sci_figure_lib.matplotlib_helpers import (
    apply_pub_bar_style,
    apply_pub_fan_style,
    apply_pub_rcparams,
    apply_pub_scatter_style,
)
from sci_figure_lib.render import (
    REVIEW_BOUNDS,
    cli_export,
    crop_review_png,
    make_review_png,
    verify_aspect_ratios,
)

__version__ = "0.1.0"

__all__ = [
    "DrawioBuilder",
    "GlyphMixin",
    "apply_pub_bar_style",
    "apply_pub_fan_style",
    "apply_pub_rcparams",
    "apply_pub_scatter_style",
    "REVIEW_BOUNDS",
    "cli_export",
    "crop_review_png",
    "make_review_png",
    "verify_aspect_ratios",
]
