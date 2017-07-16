from game import *
from itertools import product

class FullMove(collections.namedtuple("FullMove", ["first", "second"])):
    __slots__ = ()
    def __repr__(self):
        return '{' + str(self.first) + ' then ' + str(self.second) + '}'

GameState = collections.namedtuple("GameState", ["board", "turn", "children"])


def getHexMoves(board, hex, turn):
    moves = []
    for h in board:
        if -1 <= board[h] < 1 and not inHomeRow(h, turn) and hex != h:
            moves.append(Move(hex, h))
    return moves


def getFullMoves(board, turn, pieces):
    moves = []
    underAttack = getThreatened(-turn, pieces)
    pieceMoves = []
    hexMoves = []
    for i in pieces[(turn + 1) / 2]:
        for j in getPieceMoves(board, i, turn):
            pieceMoves.append(Move(i, j))
            if turn == 1: # opening hex moves from high spots
                board[i]-=turn
                board[j]+=turn
                if hexPickup(board, i, turn, True, pieces, False):
                    for k in getHexMoves(board, i, turn):
                        moves.append(FullMove(pieceMoves[-1], k))
                board[j]-=turn
                board[i]+=turn
    for hex in board:
        if hexPickup(board, hex, turn, pieceMoves != [], pieces, False):
            if turn == -1: # opening up hex moves to low spots
                for i in pieceMoves:
                    if board[i.start] == -2 and not inHomeRow(i.start, turn):
                        moves.append(FullMove(i, Move(hex, i.start)))
            for i in getHexMoves(board, hex, turn):
                hexMoves.append(i)
                if turn == -1 and board[i.start] == 0: # opening up spots for low stones
                    for j in getNeighbors(i.start):
                        if j in pieces[0]:
                            moves.append(FullMove(i, Move(j, i.start)))
                elif turn == 1 and board[i.end] == 0: # opening up spots for high stones
                    for j in getNeighbors(i.end):
                        if j in pieces[0]:
                            moves.append(FullMove(i, Move(j, i.end)))
    for i in product(hexMoves, pieceMoves):
        if i[0].start != i[1].end and i[0].end != i[0].end: # hex move would interfere
            moves.append(FullMove(i[0], i[1]))
    for i in underAttack:
        for j in hexMoves + pieceMoves:
            moves.append(FullMove(i, j))
    return moves


def score(state):
    if hasWon(state.board, not state.turn):
        return sys.maxint
    if hasWon(state.board, state.turn):
        return -sys.maxint
    temp = 0
    for h in b:
        pass


def evaluate(stateTree):
    for i in stateTree.children:
        if stateTree.turn == 1:
            pass


def executeMove(board, move):
    temp = board.copy()
    for i in move:
        if type(i) == Hex:  # capture
            temp[i] -= sign(temp[i])
        elif abs(board[i.start]) == 2:  # piece move
            temp[i.start] -= sign(temp[i.start])
            temp[i.end] += sign(temp[i.start])
        else:  # hex move
            temp[i.start] -= 1
            temp[i.end] += 1
    return board


def deepen(state):
    if state.children == []:
        state.children = [GameState(executeMove(state.board, i), not state.turn, []) for i in getFullMoves(state.board, state.turn)]
        return
    for i in state.children:
        deepen(i)