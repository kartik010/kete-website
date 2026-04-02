#!/usr/bin/env python3
"""Make pixels at or near pure black transparent (keeps dark grey letterforms)."""
import sys
from PIL import Image


def main() -> None:
    if len(sys.argv) < 3:
        print("usage: knockout_near_black.py <in.png> <out.png> [max_rgb]", file=sys.stderr)
        sys.exit(2)
    inp, outp = sys.argv[1], sys.argv[2]
    mx = int(sys.argv[3]) if len(sys.argv) > 3 else 22

    im = Image.open(inp).convert("RGBA")
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if r <= mx and g <= mx and b <= mx:
                px[x, y] = (r, g, b, 0)
    im.save(outp, "PNG", optimize=True)
    print(f"OK max_rgb<={mx} -> {outp}")


if __name__ == "__main__":
    main()
