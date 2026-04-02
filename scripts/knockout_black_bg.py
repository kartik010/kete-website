#!/usr/bin/env python3
"""Remove near-black background via edge flood-fill (same idea as clean Photoroom alpha)."""
from __future__ import annotations

import sys
from collections import deque

from PIL import Image


def color_dist(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2) ** 0.5


def corner_bg(img: Image.Image, tol_match: float = 50) -> tuple[int, int, int]:
    w, h = img.size
    px = img.load()
    corners = [
        px[0, 0][:3],
        px[w - 1, 0][:3],
        px[0, h - 1][:3],
        px[w - 1, h - 1][:3],
    ]
    # Use darkest corner cluster as background seed (typical: black bars)
    base = min(corners, key=lambda c: sum(c))
    # If corners disagree a lot, average only those close to darkest
    dark = []
    for c in corners:
        if color_dist(c, base) <= tol_match:
            dark.append(c)
    if not dark:
        dark = corners
    r = sum(x[0] for x in dark) // len(dark)
    g = sum(x[1] for x in dark) // len(dark)
    b = sum(x[2] for x in dark) // len(dark)
    return (r, g, b)


def flood_transparent(
    img: Image.Image,
    bg: tuple[int, int, int],
    tol: float,
) -> Image.Image:
    w, h = img.size
    rgba = img.convert("RGBA")
    px = rgba.load()
    visited = [[False] * w for _ in range(h)]
    q: deque[tuple[int, int]] = deque()

    def push(x: int, y: int) -> None:
        if 0 <= x < w and 0 <= y < h and not visited[y][x]:
            q.append((x, y))

    for x in range(w):
        push(x, 0)
        push(x, h - 1)
    for y in range(h):
        push(0, y)
        push(w - 1, y)

    while q:
        x, y = q.popleft()
        if visited[y][x]:
            continue
        r, g, b = px[x, y][:3]
        if color_dist((r, g, b), bg) > tol:
            continue
        visited[y][x] = True
        px[x, y] = (r, g, b, 0)
        push(x + 1, y)
        push(x - 1, y)
        push(x, y + 1)
        push(x, y - 1)

    return rgba


def main() -> None:
    if len(sys.argv) < 3:
        print("usage: knockout_black_bg.py <input.png> <output.png> [tolerance]", file=sys.stderr)
        sys.exit(2)
    inp, outp = sys.argv[1], sys.argv[2]
    tol = float(sys.argv[3]) if len(sys.argv) > 3 else 38.0

    im = Image.open(inp)
    bg = corner_bg(im)
    out = flood_transparent(im, bg, tol)
    out.save(outp, "PNG", optimize=True)
    print(f"OK {inp} -> {outp} bg={bg} tol={tol}")


if __name__ == "__main__":
    main()
