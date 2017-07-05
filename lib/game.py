from engine import *

Move = collections.namedtuple("Move", ["start", "end"])

BOARD_SIZE = 3


def createBoard():
    board = {}
    for q in range(-BOARD_SIZE, BOARD_SIZE + 1):
        for r in range(-BOARD_SIZE, BOARD_SIZE + 1):
            for s in range(-BOARD_SIZE, BOARD_SIZE + 1):
                if q + r + s == 0:
                    if abs(r) == BOARD_SIZE:
                        board[Hex(q, r, s)] = 2 * sign(r)
                    else:
                        board[Hex(q, r, s)] = 0
    return board


def getNeighbors(hex):
    temp = [i for i in hexNeighbors(hex) if hexDistance(i, Hex(0, 0, 0)) <= BOARD_SIZE]
    if hex == Hex(-BOARD_SIZE, BOARD_SIZE, 0):
        temp.append(Hex(0, BOARD_SIZE, -BOARD_SIZE))
    elif hex == Hex(0, BOARD_SIZE, -BOARD_SIZE):
        temp.append(Hex(-BOARD_SIZE, BOARD_SIZE, 0))
    elif hex == Hex(0, -BOARD_SIZE, BOARD_SIZE):
        temp.append(Hex(BOARD_SIZE, -BOARD_SIZE, 0))
    elif hex == Hex(BOARD_SIZE, -BOARD_SIZE, 0):
        temp.append(Hex(0, -BOARD_SIZE, BOARD_SIZE))
    elif hex == Hex(BOARD_SIZE, 0, -BOARD_SIZE):
        temp.append(Hex(-BOARD_SIZE, 0, BOARD_SIZE))
    elif hex == Hex(-BOARD_SIZE, 0, BOARD_SIZE):
        temp.append(Hex(BOARD_SIZE, 0, -BOARD_SIZE))
    return temp


def inHomeRow(hex, turn):
    return r == BOARD_SIZE * turn


def getPieceMoves(board, hex, turn):
    moves = []
    for i in getNeighbors(board, hex):
        if board[i] == turn and not inHomeRow(board[i], turn):
            moves.append(i)
    return moves


def getMoves(board, turn):
    moves = []
    for h in board:
        if board[h] == 2 * turn:
            moves += [Move(board[h], i) for i in getPieceMoves(board, board[h], turn)]
    return moves


def canMovePiece(board, hex, turn):
    return len(getPieceMoves(board, hex, turn)) > 0


def canMove(board, turn):
    return len(getMoves(board, turn)) > 0


def piecePickup(board, hex, turn):
    if hex in board and board[hex] == 2 * turn and canMovePiece(board, hex, turn):
        board[hex] -= turn * 2 - 1
        return True
    return False


# assumes that move.start is valid
def piecePlace(board, move, turn):
    if move.end in board and board[move.end] == turn and move.end in getNeighbors(move.start):
        board[move.end] += turn * 2 - 1
        return True
    return False


def hexPickup(board, hex, turn, movedPiece):
    if hex in board and -1 < board[hex] <= 1 and not inHomeRow(hex):
        board[hex] -= 1
        if movedPiece or canMove(board, turn):
            return True
        board[hex] += 1
    return False


# assumes that move.start is valid
def hexPlace(board, move, turn, movedPiece):
    if move.end in board and -1 <= board[move.end] < 1 and not inHomeRow(move.end):
        board[move.end] += 1
        if movedPiece or canMove(board, turn):
            return True
    board[move.start] += 1
    return False
