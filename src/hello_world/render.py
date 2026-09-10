"""Pretty, TUI-style rendering of code snippets.

Draws a rounded frame around a snippet with a titled header and a subtle
line-number gutter, in the spirit of a nice terminal UI. Uses only the
standard library so the CLI stays dependency-free.
"""

from __future__ import annotations

import os
import sys
import time

# Box-drawing characters for a rounded frame.
_TOP_LEFT = "╭"  # ╭
_TOP_RIGHT = "╮"  # ╮
_BOTTOM_LEFT = "╰"  # ╰
_BOTTOM_RIGHT = "╯"  # ╯
_HORIZONTAL = "─"  # ─
_VERTICAL = "│"  # │

# ANSI styling. Kept minimal and only emitted when color is enabled.
_RESET = "\033[0m"
_DIM = "\033[2m"
_BOLD = "\033[1m"
_CYAN = "\033[36m"

# Horizontal padding between the frame and its contents.
_PAD = 1


def _supports_color(stream) -> bool:
    """Return True when it's safe to emit ANSI colors to *stream*."""
    if os.environ.get("NO_COLOR") is not None:
        return False
    if os.environ.get("TERM") == "dumb":
        return False
    return bool(getattr(stream, "isatty", lambda: False)())


def _style(text: str, *codes: str, color: bool) -> str:
    """Wrap *text* in ANSI *codes* when *color* is enabled."""
    if not color or not codes:
        return text
    return "".join(codes) + text + _RESET


def render_lines(
    language: str,
    code: str,
    *,
    color: bool | None = None,
    stream=None,
) -> list[str]:
    """Return the framed *code* as a list of output lines (header, body, footer).

    See :func:`render_example` for the frame layout; this variant returns the
    individual rows so callers (e.g. the animator) can emit them one at a time.
    """
    if color is None:
        color = _supports_color(stream if stream is not None else sys.stdout)

    lines = code.split("\n")
    gutter_w = len(str(len(lines)))

    # Plain (uncolored) body rows, used to measure the required inner width.
    plain_rows = [f"{i:>{gutter_w}} {_VERTICAL} {line}" for i, line in enumerate(lines, 1)]

    title = f" {language} "
    inner = max(max((len(r) for r in plain_rows), default=0), len(title)) + _PAD * 2

    # Header: ╭─ title ──────╮
    styled_title = _style(title, _BOLD, _CYAN, color=color)
    header_fill = _HORIZONTAL * (inner - len(title) - 1)
    header = _style(
        _TOP_LEFT + _HORIZONTAL, _DIM, color=color
    ) + styled_title + _style(header_fill + _TOP_RIGHT, _DIM, color=color)

    # Footer: ╰──────────────╯
    footer = _style(_BOTTOM_LEFT + _HORIZONTAL * inner + _BOTTOM_RIGHT, _DIM, color=color)

    border = _style(_VERTICAL, _DIM, color=color)
    pad = " " * _PAD

    out = [header]
    for i, line in enumerate(lines, 1):
        gutter = _style(f"{i:>{gutter_w}} {_VERTICAL}", _DIM, color=color)
        content = f"{gutter} {line}"
        # Right-pad using the plain measurement so colored rows still align.
        visible_len = len(plain_rows[i - 1])
        right = " " * (inner - _PAD * 2 - visible_len)
        out.append(f"{border}{pad}{content}{right}{pad}{border}")
    out.append(footer)

    return out


def render_example(
    language: str,
    code: str,
    *,
    color: bool | None = None,
    stream=None,
) -> str:
    """Return *code* wrapped in a titled, rounded TUI frame.

    The frame header shows *language*, and each line is prefixed with a dim
    line-number gutter. When *color* is None, color is auto-detected from
    *stream* (defaulting to stdout).
    """
    return "\n".join(
        render_lines(language, code, color=color, stream=stream)
    )


def animate_example(
    language: str,
    code: str,
    *,
    color: bool | None = None,
    delay: float = 0.06,
    stream=None,
) -> None:
    """Print the framed *code* to *stream*, revealing one row at a time.

    Each row of the frame is written with a short *delay* in between, so the
    snippet appears to "unfold" line by line. When *stream* is not a TTY the
    animation is skipped and the frame is printed all at once, keeping piped
    output clean. Color is auto-detected from *stream* unless given.
    """
    if stream is None:
        stream = sys.stdout

    is_tty = bool(getattr(stream, "isatty", lambda: False)())
    rows = render_lines(language, code, color=color, stream=stream)

    if not is_tty or delay <= 0:
        stream.write("\n".join(rows) + "\n")
        stream.flush()
        return

    for row in rows:
        stream.write(row + "\n")
        stream.flush()
        time.sleep(delay)
