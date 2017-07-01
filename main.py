import collections

Hex = collections.namedtuple("Hex", ["q", "r", "s"])

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

def hexNeighbors(hex, size=999): # replace with max int
    return [i for i in [hexNeighbor(hex, j) for j in range(6)] if hexDistance(i, Hex(0,0,0)) <= size]

def createHexBoard(size):
    board = {}
    for q in range(-size, size+1):
        for r in range(-size, size+1):
            for s in range(-size, size+1):
                if q+r+s == 0:
                    board[Hex(q,r,s)] = 0
    return board

b = createHexBoard(3)
for i in hexNeighbors(Hex(3,0,-3), 3):
    print i

#print hexDistance(Hex(), Hex(0,0,0))
