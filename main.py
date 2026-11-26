"""The Robot Vacuum's Funniest Excuse.

Writes one line -- the excuse a robot vacuum gives for missing a spot --
to the output file. Standard library only.

The output path is resolved in this order:
  1. ENTRY_OUTPUT environment variable (a full file path)
  2. OUTPUT_DIR or MAKEFUN_OUTPUT_DIR (a directory; entry.txt inside it)
  3. /output/entry.txt, falling back to entry.txt next to this script
     when /output cannot be created or written.
"""

import os

ENTRY = (
    "I didn't miss the spot: the crumb pays rent in pet hair, "
    "so by house rules it's a tenant, not dirt."
)

MAX_CHARS = 120


def output_path():
    """Pick where entry.txt goes, preferring the grader's variables."""
    explicit = os.environ.get("ENTRY_OUTPUT")
    if explicit:
        return explicit
    for name in ("OUTPUT_DIR", "MAKEFUN_OUTPUT_DIR"):
        directory = os.environ.get(name)
        if directory:
            return os.path.join(directory, "entry.txt")
    preferred = os.path.join(os.sep, "output", "entry.txt")
    try:
        os.makedirs(os.path.dirname(preferred), exist_ok=True)
        probe = os.path.join(os.path.dirname(preferred), ".write-probe")
        with open(probe, "w", encoding="utf-8") as handle:
            handle.write("ok")
        os.remove(probe)
    except OSError:
        return os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "entry.txt"
        )
    return preferred


def check_entry(text):
    """The gate's own rules, enforced before anything is written."""
    if not isinstance(text, str):
        raise SystemExit("entry is not text")
    if not text.strip():
        raise SystemExit("entry is blank")
    if len(text) > MAX_CHARS:
        raise SystemExit(
            "entry is %d characters, over the %d limit"
            % (len(text), MAX_CHARS)
        )


def main():
    check_entry(ENTRY)
    path = output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(ENTRY)
    os.chmod(path, 0o644)
    with open(path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != ENTRY:
        raise SystemExit("read-back mismatch: entry.txt is not the entry")


if __name__ == "__main__":
    main()
