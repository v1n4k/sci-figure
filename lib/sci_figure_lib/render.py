"""Render + QA helpers — drawio CLI export with cleanup, aspect-ratio
guard, bounded review-PNG downsampling.

Why these live here:
- ``cli_export`` shells out to the drawio CLI and **always** kills any
  orphan ``draw.io.app`` Electron child processes afterwards. Without
  cleanup, repeated invocations accumulate background processes that
  consume RAM and can hang subsequent CLI calls.
- ``make_review_png`` downsamples the full-resolution export to a
  bounded longest-side. The hard bounds (``REVIEW_BOUNDS``) reflect
  what an agent reviewer can ingest: above ~1800 px the image-input
  rejects with "image too large"; below ~800 px sub-panel headers and
  arrow labels become unreadable.
- ``verify_aspect_ratios`` walks the produced ``.drawio`` XML, decodes
  each embedded PNG IHDR, and asserts the cell geometry matches the
  source aspect within a tolerance. Catches embed bugs at QA time.
"""

from __future__ import annotations

import base64
import platform
import shutil
import subprocess
from pathlib import Path
from xml.etree import ElementTree as ET

from PIL import Image

# --- Review-PNG sizing bounds --------------------------------------------
# Lower bound: below ~800 px the figure becomes unreadable for either
# an agent reviewer or a human at 25 % zoom.
# Upper bound: ~1800 px sits safely under Anthropic's image-input cap;
# above this an agent reviewer risks "image too large" failures.
REVIEW_BOUNDS: tuple[int, int] = (800, 1800)
DEFAULT_REVIEW_PX: int = 1500


# --- drawio CLI resolution + execution -----------------------------------

_DRAWIO_PROCESS_NAME = "draw.io"  # used by pkill -f


def _resolve_drawio_cli() -> Path:
    """Return the absolute path to the drawio CLI for this platform.

    Resolution order (in priority):
    1. ``$DRAWIO_CLI`` env var if set and exists.
    2. macOS app bundle: ``/Applications/draw.io.app/Contents/MacOS/draw.io``.
    3. ``draw.io`` or ``drawio`` on PATH (Linux / Windows / brew).
    """
    import os

    env = os.environ.get("DRAWIO_CLI")
    if env:
        p = Path(env).expanduser()
        if p.exists():
            return p

    if platform.system() == "Darwin":
        mac = Path("/Applications/draw.io.app/Contents/MacOS/draw.io")
        if mac.exists():
            return mac

    for name in ("draw.io", "drawio"):
        which = shutil.which(name)
        if which:
            return Path(which)

    raise FileNotFoundError(
        "drawio CLI not found. Set $DRAWIO_CLI, install via "
        "'brew install --cask drawio' (macOS) or your platform's package "
        "manager, and ensure 'draw.io' or 'drawio' is on PATH."
    )


def _kill_orphan_drawio_processes() -> None:
    """pkill any stray drawio Electron processes.

    The macOS drawio CLI sometimes leaves the Electron child running
    after the main process exits. We always run this in a ``finally``
    so it executes whether the export succeeded or failed.
    ``pkill`` exits non-zero when there's nothing to kill (harmless).
    """
    try:
        subprocess.run(
            ["pkill", "-f", "draw.io.app/Contents/MacOS/draw.io"],
            check=False,
            capture_output=True,
            timeout=5,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        # pkill not installed (e.g. some Windows shells) or hung — give up
        # quietly. Cleanup is best-effort.
        pass


def cli_export(
    drawio_path: Path,
    out_png: Path,
    *,
    scale: int = 3,
    timeout: int = 120,
) -> Path:
    """Export a ``.drawio`` to PNG via the drawio CLI.

    Always cleans up orphan Electron processes after the export, success
    or failure. Returns ``out_png``.

    Math notation rasterizes correctly here when the cell uses drawio's
    accepted MathJax delimiters (``\\(...\\)`` inline / ``$$...$$``
    display) — see ``sci_figure_lib.drawio_builder.tex_cell``. SVG
    export, in contrast, does NOT render math (known drawio issue);
    use PNG for any figure that contains math.
    """
    cli = _resolve_drawio_cli()
    drawio_path = Path(drawio_path)
    out_png = Path(out_png)
    out_png.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        str(cli), "-x", "-f", "png", "-s", str(scale),
        "-o", str(out_png), str(drawio_path),
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, timeout=timeout)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"drawio CLI export failed (exit {e.returncode}): "
            f"{e.stderr.decode(errors='ignore')[:300]}"
        ) from e
    finally:
        _kill_orphan_drawio_processes()
    return out_png


# --- Bounded review-PNG downsampling -------------------------------------


def make_review_png(
    src_png: Path,
    dst_png: Path,
    *,
    target_max_px: int = DEFAULT_REVIEW_PX,
) -> Path:
    """Downsample ``src_png`` so its longest side is ``target_max_px`` and save.

    Bounds (``REVIEW_BOUNDS``) are enforced at runtime: ``target_max_px``
    outside [800, 1800] raises ``ValueError`` because the result would
    be either unreadable (too small) or rejected by an agent reviewer's
    image input (too large).

    Uses LANCZOS resampling. Skips the resize if the source is already
    small enough. Returns ``dst_png``.
    """
    lo, hi = REVIEW_BOUNDS
    if not (lo <= target_max_px <= hi):
        raise ValueError(
            f"target_max_px={target_max_px} outside REVIEW_BOUNDS={REVIEW_BOUNDS}: "
            f"too small → blurry / unreadable, too large → agent reviewer hits "
            f"'image too large'. Pass {DEFAULT_REVIEW_PX} for the default."
        )
    Image.MAX_IMAGE_PIXELS = None  # full export is large but trusted
    src_png = Path(src_png)
    dst_png = Path(dst_png)
    im = Image.open(src_png)
    w, h = im.size
    longest = max(w, h)
    if longest <= target_max_px:
        new_w, new_h = w, h
    else:
        scale = target_max_px / longest
        new_w = max(1, int(round(w * scale)))
        new_h = max(1, int(round(h * scale)))
        im = im.resize((new_w, new_h), Image.LANCZOS)
    if im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGBA")
    dst_png.parent.mkdir(parents=True, exist_ok=True)
    im.save(dst_png, "PNG", optimize=True)
    print(
        f"[make_review_png] {src_png.name} {w}x{h} -> {dst_png.name} "
        f"{new_w}x{new_h} (target_max_px={target_max_px})."
    )
    return dst_png


def crop_review_png(
    src_png: Path,
    dst_png: Path,
    box: tuple[float, float, float, float],
    *,
    target_max_px: int = DEFAULT_REVIEW_PX,
) -> Path:
    """Crop a normalized region (0..1: x0, y0, x1, y1) and downsample.

    Same bounds as ``make_review_png``. Useful for inspecting individual
    sub-panels at higher effective resolution.
    """
    lo, hi = REVIEW_BOUNDS
    if not (lo <= target_max_px <= hi):
        raise ValueError(
            f"target_max_px={target_max_px} outside REVIEW_BOUNDS={REVIEW_BOUNDS}"
        )
    Image.MAX_IMAGE_PIXELS = None
    src_png = Path(src_png)
    dst_png = Path(dst_png)
    im = Image.open(src_png)
    w, h = im.size
    x0, y0, x1, y1 = box
    px = (
        int(round(x0 * w)),
        int(round(y0 * h)),
        int(round(x1 * w)),
        int(round(y1 * h)),
    )
    cropped = im.crop(px)
    cw, ch = cropped.size
    longest = max(cw, ch)
    if longest > target_max_px:
        scale = target_max_px / longest
        cropped = cropped.resize(
            (max(1, int(round(cw * scale))), max(1, int(round(ch * scale)))),
            Image.LANCZOS,
        )
    if cropped.mode not in ("RGB", "RGBA"):
        cropped = cropped.convert("RGBA")
    dst_png.parent.mkdir(parents=True, exist_ok=True)
    cropped.save(dst_png, "PNG", optimize=True)
    final_w, final_h = cropped.size
    print(
        f"[crop_review_png] {src_png.name} {box} -> {dst_png.name} "
        f"{final_w}x{final_h} (target_max_px={target_max_px})."
    )
    return dst_png


# --- Aspect-ratio guard for produced .drawio -----------------------------


def verify_aspect_ratios(xml_path: Path, *, tol: float = 0.005) -> None:
    """Walk a ``.drawio`` XML and assert every embedded PNG is at its
    true aspect ratio (within ``tol``, default 0.5 %).

    Decodes each ``image=data:image/png,...`` payload's PNG IHDR chunk
    to recover the source w/h, compares against the cell's mxGeometry,
    and raises ``SystemExit(1)`` on violations.
    """
    xml_path = Path(xml_path)
    tree = ET.parse(xml_path)
    violations: list[dict] = []
    for cell in tree.iter("mxCell"):
        style = cell.get("style", "") or ""
        if "shape=image" not in style:
            continue
        marker = "image=data:image/png,"
        idx = style.find(marker)
        if idx < 0:
            continue
        b64_start = idx + len(marker)
        b64_end = style.find(";", b64_start)
        if b64_end < 0:
            b64_end = len(style)
        prefix = style[b64_start : b64_start + 64]
        prefix += "=" * (-len(prefix) % 4)
        try:
            raw = base64.b64decode(prefix)
        except Exception:
            continue
        if len(raw) < 24 or raw[:8] != b"\x89PNG\r\n\x1a\n":
            continue
        sw = int.from_bytes(raw[16:20], "big")
        sh = int.from_bytes(raw[20:24], "big")
        if sw == 0 or sh == 0:
            continue
        geom = cell.find("mxGeometry")
        if geom is None:
            continue
        try:
            cw = float(geom.get("width", "0"))
            ch = float(geom.get("height", "0"))
        except ValueError:
            continue
        if ch <= 0:
            continue
        src_ar = sw / sh
        cell_ar = cw / ch
        drift = abs(cell_ar - src_ar) / src_ar
        if drift > tol:
            violations.append({
                "id": cell.get("id", "?"),
                "src": (sw, sh),
                "cell": (cw, ch),
                "drift_pct": drift * 100.0,
            })
    if violations:
        print(f"\n[verify_aspect_ratios] {len(violations)} violation(s) in {xml_path.name}:")
        print(f"  {'cell_id':<28} {'source':>14}   {'cell':>14}   drift")
        for v in violations:
            print(
                f"  {v['id']:<28} {v['src'][0]:>5}x{v['src'][1]:<8} "
                f"  {int(v['cell'][0]):>5}x{int(v['cell'][1]):<8}  {v['drift_pct']:>5.2f}%"
            )
        raise SystemExit(1)
    print(
        f"[verify_aspect_ratios] OK — {xml_path.name}: "
        f"all embedded images within {tol * 100:.1f}% aspect tolerance."
    )
