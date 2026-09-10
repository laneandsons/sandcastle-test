"""Tests for the TUI-style snippet renderer."""

from __future__ import annotations

import unittest

from hello_world.render import render_example


class RenderExampleTests(unittest.TestCase):
    def test_no_color_when_disabled(self) -> None:
        out = render_example("python", 'print("Hello, World!")', color=False)
        self.assertNotIn("\033[", out)

    def test_color_when_enabled(self) -> None:
        out = render_example("python", 'print("Hello, World!")', color=True)
        self.assertIn("\033[", out)

    def test_frame_lines_are_equal_width(self) -> None:
        code = 'main :: IO ()\nmain = putStrLn "Hello, World!"'
        out = render_example("haskell", code, color=False)
        widths = {len(line) for line in out.splitlines()}
        self.assertEqual(len(widths), 1, out)

    def test_header_contains_language_title(self) -> None:
        out = render_example("rust", "fn main() {}", color=False)
        self.assertIn(" rust ", out.splitlines()[0])

    def test_rounded_corners_present(self) -> None:
        out = render_example("go", "package main", color=False)
        lines = out.splitlines()
        self.assertTrue(lines[0].startswith("╭"))
        self.assertTrue(lines[0].rstrip().endswith("╮"))
        self.assertTrue(lines[-1].startswith("╰"))
        self.assertTrue(lines[-1].rstrip().endswith("╯"))

    def test_line_numbers_present(self) -> None:
        out = render_example("go", "a\nb\nc", color=False)
        body = out.splitlines()[1:-1]
        self.assertEqual(len(body), 3)
        for i, line in enumerate(body, 1):
            self.assertIn(f"{i} │", line)

    def test_every_source_line_is_rendered(self) -> None:
        code = "one\ntwo\nthree"
        out = render_example("python", code, color=False)
        for token in ("one", "two", "three"):
            self.assertIn(token, out)


if __name__ == "__main__":
    unittest.main()
