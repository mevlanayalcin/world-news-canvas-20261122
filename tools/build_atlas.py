"""Derive the compact coastline file the atlas panel draws from.

Input is Natural Earth's public-domain 1:110m land layer (ne_110m_land.geojson), kept outside the repository.
Output is tools/atlas_land.json: one line, a list of rings, each ring a flat list of integers
[lon*10, lat*10, lon*10, lat*10, ...]. Antarctica and specks too small to show at atlas scale are dropped and
every ring is thinned with Douglas-Peucker so the file stays small.

    python3 tools/build_atlas.py /path/to/ne_110m_land.geojson
"""

import json
import os
import sys

TOLERANCE_DEG = 0.22  # Douglas-Peucker tolerance; well under one atlas pixel (about 0.75 degrees)
MIN_BOX_DEG2 = 2.2  # drop islands whose bounding box is smaller than this
SOUTH_LIMIT = -60.0  # rings entirely south of this are Antarctica


def point_segment_distance(p, a, b):
    """Distance in degrees from point p to segment a-b."""
    ax, ay = a
    bx, by = b
    px, py = p
    dx, dy = bx - ax, by - ay
    if dx == 0 and dy == 0:
        return ((px - ax) ** 2 + (py - ay) ** 2) ** 0.5
    t = ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)
    t = max(0.0, min(1.0, t))
    qx, qy = ax + t * dx, ay + t * dy
    return ((px - qx) ** 2 + (py - qy) ** 2) ** 0.5


def thin(points, tolerance):
    """Douglas-Peucker without recursion (rings can be long)."""
    keep = [False] * len(points)
    keep[0] = keep[-1] = True
    stack = [(0, len(points) - 1)]
    while stack:
        first, last = stack.pop()
        worst, index = 0.0, -1
        for i in range(first + 1, last):
            d = point_segment_distance(points[i], points[first], points[last])
            if d > worst:
                worst, index = d, i
        if index >= 0 and worst > tolerance:
            keep[index] = True
            stack.append((first, index))
            stack.append((index, last))
    return [p for p, k in zip(points, keep) if k]


def main():
    source = sys.argv[1]
    with open(source, encoding="utf-8") as handle:
        collection = json.load(handle)

    rings = []
    for feature in collection["features"]:
        geometry = feature["geometry"]
        polygons = geometry["coordinates"] if geometry["type"] == "MultiPolygon" else [geometry["coordinates"]]
        for polygon in polygons:
            outer = [(float(x), float(y)) for x, y in polygon[0]]
            lons = [p[0] for p in outer]
            lats = [p[1] for p in outer]
            if max(lats) < SOUTH_LIMIT:
                continue
            if (max(lons) - min(lons)) * (max(lats) - min(lats)) < MIN_BOX_DEG2:
                continue
            half = len(outer) // 2  # thin the two halves so a closed ring keeps its shape
            thinned = thin(outer[: half + 1], TOLERANCE_DEG)[:-1] + thin(outer[half:], TOLERANCE_DEG)
            if len(thinned) < 4:
                continue
            flat = []
            for lon, lat in thinned:
                flat.append(int(round(lon * 10)))
                flat.append(int(round(lat * 10)))
            rings.append(flat)

    rings.sort(key=len, reverse=True)
    target = os.path.join(os.path.dirname(os.path.abspath(__file__)), "atlas_land.json")
    with open(target, "w", encoding="utf-8") as handle:
        json.dump(rings, handle, separators=(",", ":"))
        handle.write("\n")
    print(f"{len(rings)} rings, {sum(len(r) for r in rings) // 2} points -> {target}")


if __name__ == "__main__":
    main()
