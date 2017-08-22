from engine import *
from config import *


class Move(collections.namedtuple("Move", ["start", "end"])):
    __slots__ = ()

    def __repr__(self):
        return str(self.start) + '->' + str(self.end)


def createBoard(boardSize):
    board = {}
    for q in range(-boardSize, boardSize + 1):
        for r in range(-boardSize, boardSize + 1):
            for s in range(-boardSize, boardSize + 1):
                if q + r + s == 0:
                    if abs(r) == boardSize:
                        board[Hex(q, r, s)] = 2 * sign(r)
                    else:
                        board[Hex(q, r, s)] = 0
    return board


def getNeighbors(hex):
    temp = [i for i in hexNeighbors(hex) if hexDistance(i, Hex(0, 0, 0)) <= BOARD_SIZE]
    teleports = (Hex(-BOARD_SIZE, BOARD_SIZE, 0), Hex(0, BOARD_SIZE, -BOARD_SIZE), Hex(0, -BOARD_SIZE, BOARD_SIZE), Hex(BOARD_SIZE, -BOARD_SIZE, 0), Hex(BOARD_SIZE, 0, -BOARD_SIZE), Hex(-BOARD_SIZE, 0, BOARD_SIZE))
    for i in range(6):
        if hex == teleports[i] and teleports[i] not in temp:
            if i % 2 == 0:
                temp.append(teleports[i + 1])
            else:
                temp.append(teleports[i - 1])
    return temp


def inHomeRow(hex, turn):
    return hex.r == BOARD_SIZE * turn


def getPieceMoves(board, hex, turn):
    moves = []
    for i in getNeighbors(hex):
        if board[i] == turn:
            moves.append(i)
    return moves


def getMoves(board, turn, pieces):
    moves = []
    for i in pieces[(turn + 1) / 2]:
        moves += [Move(i, j) for j in getPieceMoves(board, i, turn)]
    return moves


def canMovePiece(board, hex, turn):
    return len(getPieceMoves(board, hex, turn)) > 0


def canMove(board, turn, pieces):
    return len(getMoves(board, turn, pieces)) > 0


def piecePickup(board, hex, turn, changeBoard=True):
    if hex in board and board[hex] == 2 * turn and canMovePiece(board, hex, turn):
        if changeBoard:
            board[hex] -= sign(turn)
        return True
    return False


# assumes that move.start is valid
def piecePlace(board, move, turn, changeBoard=True):
    if move.end in getPieceMoves(board, move.start, turn):
        if changeBoard:
            board[move.end] = 2 * sign(turn)
        return True
    if changeBoard:
        board[move.start] += turn
    return False


def hexPickup(board, hex, turn, movedPiece, pieces, changeBoard=True):
    if hex in board and -1 < board[hex] <= 1 and not inHomeRow(hex, turn):
        board[hex] -= 1
        if movedPiece or turn == 1 or canMove(board, turn, pieces):
            if not changeBoard:
                board[hex] += 1
            return True
        board[hex] += 1
    return False


# assumes that move.start is valid
def hexPlace(board, move, turn, movedPiece, pieces, changeBoard=True):
    if move.end in board and -1 <= board[move.end] < 1 and not inHomeRow(move.end, turn) and move.start != move.end:
        board[move.end] += 1
        if movedPiece or canMove(board, turn, pieces):
            if not changeBoard:
                board[move.end] -= 1
            return True
        board[move.end] -= 1
    if changeBoard:
        board[move.start] += 1
    return False


def getPieces(board):
    pieces = ([], [])
    for h in board:
        if abs(board[h]) == 2:
            pieces[(board[h] + 2) / 4].append(h)
    return pieces


def getThreatened(turn, pieces):
    temp = []
    for i in pieces[(-turn + 1) / 2]:
        if [j in pieces[(turn + 1) / 2] for j in getNeighbors(i)].count(True) >= 2:
            temp.append(i)
    return temp


def hasWon(pieces):
    for i in range(2):
        if pieces[i] == []:
            return i * 2 - 1
        for j in pieces[i]:
            if inHomeRow(j, -(i * 2 - 1)):
                return i * 2 - 1
    return 0
