from game import *

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
        pieceMoves += [Move(i, j) for j in getPieceMoves(board, i, turn)]
    for hex in board:
        if hexPickup(board, hex, turn, pieceMoves != [], pieces, False):
            hexMoves += getHexMoves(board, hex, turn)

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
