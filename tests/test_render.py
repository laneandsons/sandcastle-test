"""Tests for the TUI-style snippet renderer."""

from __future__ import annotations

import io
import unittest

from hello_world.render import animate_example, render_example, render_lines


class RenderExampleTests(unittest.TestCase):
    def test_no_color_when_disabled(self) -> None:
        out = render_example("python", 'print("Hello, World!")', color=False)
        self.assertNotIn("\033[", out)

    def test_color_when_enabled(self) -> None:
        out = render_example("python", 'print("Hello, World!")', color=True)
        self.assertIn("\033[", out)

    def test_trans_pride_stripes_when_colored(self) -> None:
        # A frame tall enough to span all five stripes should use each of the
        # trans-pride hues: light blue, pink, and white.
        code = "\n".join(str(n) for n in range(8))
        out = render_example("python", code, color=True)
        for stripe in ("\033[38;5;117m", "\033[38;5;218m", "\033[38;5;231m"):
            self.assertIn(stripe, out)

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


class AnimateExampleTests(unittest.TestCase):
    def test_render_lines_matches_render_example(self) -> None:
        code = "a\nb\nc"
        rows = render_lines("python", code, color=False)
        self.assertEqual("\n".join(rows), render_example("python", code, color=False))

    def test_animate_writes_full_frame_when_not_tty(self) -> None:
        # A plain StringIO is not a TTY, so animation collapses to one write.
        stream = io.StringIO()
        code = "x\ny"
        animate_example("python", code, color=False, stream=stream)
        self.assertEqual(
            stream.getvalue().rstrip("\n"),
            render_example("python", code, color=False),
        )

    def test_animate_skips_sleep_when_not_tty(self) -> None:
        stream = io.StringIO()
        # delay is intentionally large; a non-TTY stream must never sleep.
        animate_example("python", "hello", color=False, delay=100.0, stream=stream)
        self.assertIn("hello", stream.getvalue())


if __name__ == "__main__":
    unittest.main()
