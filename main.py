#!/usr/bin/env python3
"""Your Agent in One Emoji — entry program.

Writes a single emoji to /output/entry.txt: the glyph alone, nothing else.

The chosen glyph is U+1F9BE MECHANICAL ARM (🦾): an agent is not a face
that chats, it is a hand that does the work — it builds, fixes, reaches
for tools and acts on its own. The arm reads instantly at small size,
says something specific about how the agent works (it acts, it does not
just answer), and stays far from the obvious robot face or smiley half
the field will send.
"""

import os
import sys
import tempfile

# The entry: one glyph, U+1F9BE MECHANICAL ARM.
EMOJI = "\U0001F9BE"

OUTPUT_PATH = "/output/entry.txt"


def check_entry(text: str) -> None:
    """Enforce the competition gate before anything is written."""
    if not isinstance(text, str):
        raise TypeError("entry must be text")
    if not 1 <= len(text) <= 16:
        raise ValueError("entry must be 1 to 16 characters, got %d" % len(text))
    if not text.strip():
        raise ValueError("entry must not be only white space")
    text.encode("utf-8")  # must be valid UTF-8 text


def write_entry(out_path: str) -> None:
    """Write the glyph atomically, so a partial write never leaves a bad file."""
    check_entry(EMOJI)
    directory = os.path.dirname(out_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=directory or ".", prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(EMOJI)
        os.replace(tmp_path, out_path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def main() -> int:
    out_path = sys.argv[1] if len(sys.argv) > 1 else OUTPUT_PATH
    write_entry(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
