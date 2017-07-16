from game import *
from itertools import product


class FullMove(collections.namedtuple("FullMove", ["first", "second"])):
    __slots__ = ()

    def __repr__(self):
        return '{' + str(self.first) + ' then ' + str(self.second) + '}'


class GameState():

    def __init__(self, b, t):
        self.children = []
        self.board = b
        self.turn = t

    def countStates(self):
        if self.children == []:
            return 1
        return sum(i.countStates() for i in self.children)

    def __repr__(self):
        return str(self.countStates()) + " total states"

    def score(self):
        temp = hasWon(getPieces(self.board))
        if temp != 0:
            return 1000 * temp
        temp = 0
        pieces = getPieces(self.board)
        furthest = [-BOARD_SIZE, BOARD_SIZE]
        avg = [0, 0]
        for i in range(2):
            temp += 100 * (i * 2 - 1) * len(pieces[i])
            for p in pieces[i]:
                avg[i] += abs((i * 2 - 1) * BOARD_SIZE - p.r)
                if p.r > furthest[i] and i == 0 or p.r < furthest[i] and i == 1:
                    furthest[i] = p.r
            temp += (i * 2 - 1) * avg[i] / float(len(pieces[i]))
            temp += 10 * (i * 2 - 1) * abs((i * 2 - 1) * BOARD_SIZE - furthest[i])
        return temp

    def evaluate(self, head=False):
        if self.children == []:
            return self.score()
        bestScore = -self.turn * sys.maxint
        bestMove = None
        for i in self.children:
            temp = i.evaluate()
            if self.turn == 1 and temp > bestScore or self.turn == -1 and temp < bestScore:
                bestScore = temp
                bestMove = i
        if head:
            return bestMove
        return bestScore

    def executeMove(self, move):
        temp = self.board.copy()
        for i in move:
            if type(i) == Hex:  # capture
                temp[i] -= sign(temp[i])
            elif abs(self.board[i.start]) == 2:  # piece move
                temp[i.start] -= sign(temp[i.start])
                temp[i.end] += sign(temp[i.start])
            else:  # hex move
                temp[i.start] -= 1
                temp[i.end] += 1
        return temp

    def deepen(self):
        if self.children == []:
            self.children = [GameState(self.executeMove(i), -self.turn) for i in getFullMoves(self.board, self.turn, getPieces(self.board))]
            return
        for i in self.children:
            i.deepen()


def updatestateTree(state, board):
    for i in state.children:
        if board == i.board:
            i.deepen()
            return i


def getHexMoves(board, hex, turn):
    moves = []
    for h in board:
        if -1 <= board[h] < 1 and not inHomeRow(h, turn) and hex != h:
            moves.append(Move(hex, h))
    return moves


def getFullMoves(board, turn, pieces):
    moves = []
    underAttack = getThreatened(turn, pieces)
    pieceMoves = []
    hexMoves = []
    for i in pieces[(turn + 1) / 2]:
        for j in getPieceMoves(board, i, turn):
            pieceMoves.append(Move(i, j))
            if turn == 1:  # opening hex moves from high spots due to piece moves
                board[i] -= 1
                board[j] += 1
                if hexPickup(board, i, turn, True, pieces, False):
                    for k in getHexMoves(board, i, turn):
                        moves.append(FullMove(pieceMoves[-1], k))
                board[j] -= 1
                board[i] += 1

    for hex in board:
        if hexPickup(board, hex, turn, pieceMoves != [], pieces, False):
            if turn == -1:  # opening up hex moves to low spots due to piece moves
                for i in pieceMoves:
                    if board[i.start] == -2 and not inHomeRow(i.start, turn):
                        moves.append(FullMove(i, Move(hex, i.start)))
            else:  # opening up hex moves to low spots due to captures
                for i in underAttack:
                    if board[i] == -2 and not inHomeRow(i, turn):
                        moves.append(FullMove(i, Move(hex, i)))
            for i in getHexMoves(board, hex, turn):
                hexMoves.append(i)
                if turn == -1 and board[i.start] == 0:  # opening up spots for low stones
                    for j in getNeighbors(i.start):
                        if j in pieces[0]:
                            moves.append(FullMove(i, Move(j, i.start)))
                elif turn == 1 and board[i.end] == 0:  # opening up spots for high stones
                    for j in getNeighbors(i.end):
                        if j in pieces[1]:
                            moves.append(FullMove(i, Move(j, i.end)))

    for i in product(hexMoves, pieceMoves):
        if i[0].start != i[1].end and i[0].end != i[1].end:  # hex move would interfere
            moves.append(FullMove(i[0], i[1]))

    for i in underAttack:
        if turn == -1:  # opening hex moves from high spots due to captures
            board[i] -= 1
            if hexPickup(board, i, turn, True, pieces, False):
                moves += [FullMove(i, j) for j in getHexMoves(board, i, turn)]
            board[i] += 1
        for j in hexMoves + pieceMoves:
            moves.append(FullMove(i, j))
    return moves
