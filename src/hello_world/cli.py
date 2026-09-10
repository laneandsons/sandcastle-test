"""A tiny CLI that prints a 'Hello, World!' example for a given language."""

from __future__ import annotations

import argparse
import sys

from hello_world.render import animate_example, render_example

# Each entry maps a language name to a ready-to-run "Hello, World!" snippet.
EXAMPLES: dict[str, str] = {
    "gleam": '''import gleam/io

pub fn main() {
  io.println("Hello, World!")
}''',
    "haskell": '''main :: IO ()
main = putStrLn "Hello, World!"''',
    "python": '''print("Hello, World!")''',
    "javascript": '''console.log("Hello, World!");''',
    "typescript": '''const greeting: string = "Hello, World!";
console.log(greeting);''',
    "rust": '''fn main() {
    println!("Hello, World!");
}''',
    "go": '''package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}''',
    "ruby": '''puts "Hello, World!"''',
    "java": '''public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}''',
    "c": '''#include <stdio.h>

int main(void) {
    printf("Hello, World!\\n");
    return 0;
}''',
}

# Friendly aliases so common spellings still resolve.
ALIASES: dict[str, str] = {
    "js": "javascript",
    "ts": "typescript",
    "rs": "rust",
    "golang": "go",
    "py": "python",
    "hs": "haskell",
}


def resolve(name: str) -> str | None:
    """Normalize a language name and return its canonical key, if known."""
    key = name.strip().lower()
    key = ALIASES.get(key, key)
    return key if key in EXAMPLES else None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hello-world",
        description="Print a 'Hello, World!' example in a given language.",
    )
    parser.add_argument(
        "language",
        nargs="?",
        help="the language to print an example for (e.g. gleam, haskell, python)",
    )
    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="list all supported languages and exit",
    )
    parser.add_argument(
        "-p",
        "--plain",
        action="store_true",
        help="print the raw snippet without the decorative frame",
    )
    parser.add_argument(
        "-a",
        "--animate",
        action="store_true",
        help="reveal the framed snippet one line at a time (skipped when piped)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list:
        print("Supported languages:")
        for name in sorted(EXAMPLES):
            print(f"  {name}")
        return 0

    if not args.language:
        parser.print_help(sys.stderr)
        return 1

    key = resolve(args.language)
    if key is None:
        print(
            f"Unknown language: {args.language!r}. "
            f"Try one of: {', '.join(sorted(EXAMPLES))}.",
            file=sys.stderr,
        )
        return 1

    code = EXAMPLES[key]
    if args.plain:
        print(code)
    elif args.animate:
        animate_example(key, code)
    else:
        print(render_example(key, code))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
