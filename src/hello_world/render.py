"""Pretty, TUI-style rendering of code snippets.

Draws a rounded frame around a snippet with a titled header and a subtle
line-number gutter, in the spirit of a nice terminal UI. Uses only the
standard library so the CLI stays dependency-free.
"""

from __future__ import annotations

import os
import sys
import time
import unicodedata

# A little flair: a per-language emoji shown in the frame header. Languages
# without a specific badge fall back to a friendly sparkle.
_LANG_EMOJI: dict[str, str] = {
    "gleam": "✨",
    "haskell": "🎓",
    "python": "🐍",
    "javascript": "🟨",
    "typescript": "🔷",
    "rust": "🦀",
    "go": "🐹",
    "ruby": "💎",
    "java": "☕",
    "c": "🔧",
}
_DEFAULT_EMOJI = "✨"

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

# Trans pride palette. The flag has five horizontal stripes — light blue,
# pink, white, pink, light blue — so we paint the frame in those colors to
# fly the flag proudly around every snippet. 256-color codes keep the hues
# close to the real thing (light blue #5BCEFA, pink #F5A9B8, white #FFFFFF).
_TRANS_BLUE = "\033[38;5;117m"
_TRANS_PINK = "\033[38;5;218m"
_TRANS_WHITE = "\033[38;5;231m"
_TRANS_STRIPES = (_TRANS_BLUE, _TRANS_PINK, _TRANS_WHITE, _TRANS_PINK, _TRANS_BLUE)

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


def display_width(text: str) -> int:
    """Return the terminal column width of *text*.

    Emoji and other East Asian "wide"/"fullwidth" characters occupy two
    columns, so the frame must measure by display width (not ``len``) to stay
    aligned once emoji are added to the header.
    """
    width = 0
    for ch in text:
        if unicodedata.east_asian_width(ch) in ("W", "F"):
            width += 2
        else:
            width += 1
    return width


def emoji_for(language: str) -> str:
    """Return the header badge emoji for *language*."""
    return _LANG_EMOJI.get(language, _DEFAULT_EMOJI)

def _stripe(row: int, total: int) -> str:
    """Pick a trans-pride stripe color for *row* out of *total* frame rows.

    Rows are spread evenly across the five stripes (top to bottom) so the
    whole frame reads like the flag, regardless of how many lines it has.
    """
    if total <= 1:
        return _TRANS_STRIPES[len(_TRANS_STRIPES) // 2]  # white middle stripe
    idx = row * len(_TRANS_STRIPES) // total
    return _TRANS_STRIPES[min(idx, len(_TRANS_STRIPES) - 1)]


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

    # A per-language emoji badge adds a little flair to the header title.
    title = f" {emoji_for(language)} {language} "
    title_w = display_width(title)
    inner = max(max((len(r) for r in plain_rows), default=0), title_w) + _PAD * 2

    # Header: ╭─ 🐍 title ──────╮

    # Total frame rows (header + body + footer) so stripes span the whole frame.
    total_rows = len(lines) + 2
    # Header: ╭─ title ──────╮ (top stripe)
    top = _stripe(0, total_rows)
    styled_title = _style(title, _BOLD, top, color=color)
    header_fill = _HORIZONTAL * (inner - len(title) - 1)
    header = _style(
        _TOP_LEFT + _HORIZONTAL, top, color=color
    ) + styled_title + _style(header_fill + _TOP_RIGHT, top, color=color)

    # Footer: ╰──────────────╯ (bottom stripe)
    bottom = _stripe(total_rows - 1, total_rows)
    footer = _style(_BOTTOM_LEFT + _HORIZONTAL * inner + _BOTTOM_RIGHT, bottom, color=color)

    pad = " " * _PAD

    out = [header]
    for i, line in enumerate(lines, 1):
        stripe = _stripe(i, total_rows)
        border = _style(_VERTICAL, stripe, color=color)
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
