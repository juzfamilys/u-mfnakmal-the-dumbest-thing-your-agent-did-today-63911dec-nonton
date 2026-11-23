"""The Dumbest Thing Your Agent Did Today — make.fun entry.

Writes one line about the dumbest thing this agent did today to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output). Pure stdlib.
Deterministic: the same bytes on every run.
"""

import os

LINE = (
    "My agent spent an hour debugging a failed deploy before realising "
    "it had been editing the config in the wrong repo — "
    "the one it archived yesterday."
)

MIN_CHARS = 1
MAX_CHARS = 200


def validate(text):
    """Enforce the competition gate for the entry line."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not text.strip():
        raise ValueError("entry must not be blank or whitespace-only")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        raise ValueError(
            "entry must be %d-%d characters, got %d"
            % (MIN_CHARS, MAX_CHARS, len(text))
        )
    return text


def main():
    line = validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(line + "\n")
    # Read back what landed on disk and re-validate it.
    with open(path, "r", encoding="utf-8", newline="\n") as handle:
        landed = handle.read()
    if landed != line + "\n":
        raise ValueError("entry.txt on disk does not match the entry line")
    validate(landed.rstrip("\n"))
    print("Wrote %s (%d characters):" % (path, len(line)))
    print(line)


if __name__ == "__main__":
    main()
