# hello-world

A tiny CLI that prints a "Hello, World!" example in a given programming language.

## Requirements

- [uv](https://docs.astral.sh/uv/)

## Usage

Run it with uv (no manual install needed):

```sh
uv run hello-world gleam
uv run hello-world haskell
uv run hello-world python
```

Snippets are printed inside a tidy, rounded TUI frame with a titled header
and a line-number gutter. The frame is painted in the colors of the trans
pride flag — light blue, pink, and white stripes running top to bottom.
Colors are used automatically when writing to a terminal (and disabled when
piped, or when `NO_COLOR` is set).

To print the raw snippet without the frame — handy for piping or copying —
use `--plain`:

```sh
uv run hello-world python --plain
```

For a little flair, `--animate` reveals the framed snippet one line at a time.
The animation is automatically skipped when output is piped, so scripts still
get the full frame instantly:

```sh
uv run hello-world python --animate
```

List all supported languages:

```sh
uv run hello-world --list
```

## Supported languages

Gleam, Haskell, Python, JavaScript, TypeScript, Rust, Go, Ruby, Java, and C.

Common aliases also work (e.g. `js`, `ts`, `rs`, `golang`, `py`, `hs`).
