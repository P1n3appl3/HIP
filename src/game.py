from engine import *
from config import *

Move = collections.namedtuple("Move", ["start", "end"])

FullMove = collections.namedtuple("FullMove", ["hex", "piece"])


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
    return hex.r == BOARD_SIZE * turn


def getPieceMoves(board, hex, turn):
    moves = []
    for i in getNeighbors(hex):
        if board[i] == turn and (not inHomeRow(i, turn) or inHomeRow(hex, turn)):
            moves.append(i)
    return moves


def getMoves(board, turn):
    moves = []
    for h in board:
        if board[h] == 2 * turn:
            moves += [Move(board[h], i) for i in getPieceMoves(board, h, turn)]
    return moves


def canMovePiece(board, hex, turn):
    return len(getPieceMoves(board, hex, turn)) > 0


def canMove(board, turn):
    return len(getMoves(board, turn)) > 0


def piecePickup(board, hex, turn):
    if hex in board and board[hex] == 2 * turn and canMovePiece(board, hex, turn):
        board[hex] -= sign(turn)
        return True
    return False


# assumes that move.start is valid
def piecePlace(board, move, turn):
    if move.end in board and board[move.end] == turn and (not inHomeRow(move.end, turn) or inHomeRow(move.start, turn)) and move.end in getNeighbors(move.start):
        board[move.end] = 2 * sign(turn)
        return True
    board[move.start] += turn
    return False


def hexPickup(board, hex, turn, movedPiece):
    if hex in board and -1 < board[hex] <= 1 and not inHomeRow(hex, turn):
        board[hex] -= 1
        if movedPiece or turn == 1 or canMove(board, turn):
            return True
        board[hex] += 1
    return False


# assumes that move.start is valid
def hexPlace(board, move, turn, movedPiece):
    if move.end in board and -1 <= board[move.end] < 1 and not inHomeRow(move.end, turn) and move.start != move.end:
        board[move.end] += 1
        if movedPiece or canMove(board, turn):
            return True
        board[move.end] -= 1
    board[move.start] += 1
    return False


def getThreatened(board, turn):
    temp = []
    for h in board:
        if board[h] == -2 * turn and [board[i] for i in getNeighbors(h)].count(2 * turn) >= 2:
            temp.append(h)
    return temp


def hasWon(board, turn):
    enemyHasPiece = False
    for h in board:
        if board[h] == -2 * turn:
            enemyHasPiece = True
        if board[h] == 2 * turn and inHomeRow(h, -turn):
            return True
    return not enemyHasPiece
