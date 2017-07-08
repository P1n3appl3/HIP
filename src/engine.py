import sys
import math
import collections

Hex = collections.namedtuple("Hex", ["q", "r", "s"])

Point = collections.namedtuple("Point", ["x", "y"])

Orientation = collections.namedtuple("Orientation", ["f0", "f1", "f2", "f3", "b0", "b1", "b2", "b3", "startAngle"])

Layout = collections.namedtuple("Layout", ["orientation", "size", "origin"])


def sign(x): return 1 if x > 0 else 0 if x == 0 else -1


def addHex(a, b):
    return Hex(a.q + b.q, a.r + b.r, a.s + b.s)


def subHex(a, b):
    return Hex(a.q + b.q, a.r + b.r, a.s + b.s)


def hexDirection(direction):
    return [Hex(1, 0, -1), Hex(1, -1, 0), Hex(0, -1, 1), Hex(-1, 0, 1), Hex(-1, 1, 0), Hex(0, 1, -1)][direction]


def hexNeighbor(hex, direction):
    return addHex(hex, hexDirection(direction))


def hexLength(hex):
    return (abs(hex.q) + abs(hex.r) + abs(hex.s)) // 2


def hexDistance(a, b):
    return hexLength(subHex(a, b))


def hexNeighbors(hex):
    return [hexNeighbor(hex, j) for j in range(6)]


def hexRound(h):
    q = int(round(h.q))
    r = int(round(h.r))
    s = int(round(h.s))
    q_diff = abs(q - h.q)
    r_diff = abs(r - h.r)
    s_diff = abs(s - h.s)
    if q_diff > r_diff and q_diff > s_diff:
        q = -r - s
    else:
        if r_diff > s_diff:
            r = -q - s
        else:
            s = -q - r
    return Hex(q, r, s)


def hexToPixel(layout, h):
    M = layout.orientation
    size = layout.size
    origin = layout.origin
    x = (M.f0 * h.q + M.f1 * h.r) * size.x
    y = (M.f2 * h.q + M.f3 * h.r) * size.y
    return Point(x + origin.x, y + origin.y)


def pixelToHex(layout, p, round=True):
    M = layout.orientation
    size = layout.size
    origin = layout.origin
    pt = Point((p.x - origin.x) / size.x, (p.y - origin.y) / size.y)
    q = M.b0 * pt.x + M.b1 * pt.y
    r = M.b2 * pt.x + M.b3 * pt.y
    if round:
        return hexRound(Hex(q, r, -q - r))
    return Hex(q, r, -q - r)


def hexCornerOffset(layout, corner):
    M = layout.orientation
    size = layout.size
    angle = 2.0 * math.pi * (M.startAngle - corner) / 6
    return Point(size.x * math.cos(angle), size.y * math.sin(angle))


def polygonCorners(layout, h):
    corners = []
    center = hexToPixel(layout, h)
    for i in range(0, 6):
        offset = hexCornerOffset(layout, i)
        corners.append(Point(center.x + offset.x, center.y + offset.y))
    return corners
