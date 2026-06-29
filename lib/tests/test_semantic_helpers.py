from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

from sci_figure_lib.drawio_builder import DrawioBuilder
from sci_figure_lib.glyphs import GlyphMixin
from sci_figure_lib.layout import Rect, union_rects


class FigureBuilder(DrawioBuilder, GlyphMixin):
    pass


class RectTests(unittest.TestCase):
    def test_split_inset_snap_union(self) -> None:
        rect = Rect(3, 7, 100, 50)
        self.assertEqual(rect.right, 103)
        self.assertEqual(rect.bottom, 57)
        self.assertEqual(rect.inset(3, 7, 10, 5), Rect(6, 14, 87, 38))
        self.assertEqual(rect.snap(10), Rect(0, 10, 100, 50))

        left, right = Rect(0, 0, 100, 40).split_h([1, 3], gap=10)
        self.assertEqual(left, Rect(0, 0, 22.5, 40))
        self.assertEqual(right, Rect(32.5, 0, 67.5, 40))

        top, bottom = Rect(0, 0, 40, 100).split_v([2, 1], gap=10)
        self.assertEqual(top, Rect(0, 0, 40, 60))
        self.assertEqual(bottom, Rect(0, 70, 40, 30))

        self.assertEqual(
            union_rects([Rect(10, 20, 30, 40), Rect(0, 25, 5, 10)]),
            Rect(0, 20, 40, 40),
        )


class DrawioSemanticHelperTests(unittest.TestCase):
    def test_edge_points_and_label_offset(self) -> None:
        d = DrawioBuilder(page_w=400, page_h=240)
        a = d.cell("A", 20, 20, 80, 40, "rounded=1;whiteSpace=wrap;html=1;")
        b = d.cell("B", 260, 160, 80, 40, "rounded=1;whiteSpace=wrap;html=1;")
        d.edge(a, b, "flow", points=[(160, 40), (160, 180)], label_offset=(12, -18))

        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "edge.drawio"
            d.write(out)
            root = ET.parse(out).getroot()

        edge = next(cell for cell in root.iter("mxCell") if cell.get("edge") == "1")
        geom = edge.find("mxGeometry")
        self.assertIsNotNone(geom)
        self.assertEqual(len(list(geom.findall("./Array/mxPoint"))), 2)
        self.assertIsNotNone(geom.find("./mxPoint[@as='offset']"))

    def test_semantic_boxes_and_glyphs_write_valid_xml(self) -> None:
        d = FigureBuilder(page_w=800, page_h=420)
        panel_id, inner = d.panel_box(Rect(20, 20, 760, 360), "Semantic panel", tag="[A]")
        d.wrapper_box(inner.inset(10, 10, 400, 200), "iterative core")
        d.block_arrow(Rect(330, 180, 120, 34), label="split")
        d.distribution_bar_strip(
            470,
            80,
            230,
            120,
            ["A", "B", "C"],
            [0.8, 0.35, 0.2],
            title="posterior",
        )
        d.readout_list(470, 230, 230, 110, "uses", ["prediction", "target"])
        d.stacked_backplates(80, 220, 160, 80, count=3)

        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "semantic.drawio"
            d.write(out)
            root = ET.parse(out).getroot()

        self.assertTrue(panel_id.startswith("panel_bg_"))
        self.assertGreaterEqual(len(list(root.iter("mxCell"))), 20)


if __name__ == "__main__":
    unittest.main()
