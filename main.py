import pygame
import random
from src.ai import *

AVERAGEGAMELENGTH = 0
GAMESPLAYED = 0
AVERAGEMOVES = 0


def removePiece(hex, pieces):
    for i in range(len(pieces)):
        for j in range(len(pieces[i])):
            if pieces[i][j] == hex:
                del pieces[i][j]
                return


def drawHex(surface, color, layout, hex, width=0):
    x, y = tuple(hexToPixel(layout, hex))
    if width == 0:
        pygame.draw.polygon(surface, color, polygonCorners(layout, hex))
    else:
        pygame.draw.aalines(surface, color, width, polygonCorners(layout, hex))


def drawBoard(surface, outlineColor, hexColor, layout, board, coords=False):
    color = (hexColor, tuple([min(i + 40, 255) for i in hexColor]), tuple([max(i - 40, 0) for i in hexColor]))
    for h in board:
        drawHex(surface, color[sign(board[h])], layout, h)
        temp = hexToPixel(layout, h)
        if abs(board[h]) == 2:
            c = (None, 0, 255)[sign(board[h])]
            pygame.draw.circle(surface, (c, c, c), (int(temp.x), int(temp.y)), int(layout.size[0] / 2))
        if coords:
            words = pygame.font.SysFont(FONT, 16).render(str(h), 0, HINT_COLOR)
            surface.blit(words, (temp.x - words.get_width() / 2, temp.y - words.get_height() / 2))
    for h in board:
        drawHex(surface, outlineColor, layout, h, 2)


def reset(surface, text, layout, board):
    words = pygame.font.SysFont(FONT, FONT_SIZE).render(text, 0, TEXT_COLOR)
    while True:
        windowSurface.fill(BACKGROUND_COLOR)
        drawBoard(windowSurface, BACKGROUND_COLOR, BOARD_COLOR, layout, board)
        surface.blit(words, (WINDOW_WIDTH / 2 - words.get_width() / 2, WINDOW_HEIGHT / 2 - words.get_height() / 2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                return True
            elif event.type == pygame.QUIT:
                return False


def main():
    global AVERAGEGAMELENGTH
    global GAMESPLAYED
    global AVERAGEMOVES
    b = createBoard()
    turn = 1

    l = Layout(Orientation(math.sqrt(3.0), math.sqrt(3.0) / 2.0, 0.0, 3.0 / 2.0, math.sqrt(3.0) / 3.0, -1.0 / 3.0, 0.0, 2.0 / 3.0, 0.5), Point(HEX_SIZE, HEX_SIZE), Point(WINDOW_WIDTH / 2., WINDOW_HEIGHT / 2.))
    clock = pygame.time.Clock()
    movedHex = False
    movedPiece = False
    captured = False
    selected = None
    underAttack = []
    selectedColor = None
    holdingPiece = False
    currentMove = []
    pieces = getPieces(b)

    state = GameState(b, turn)
    state.deepen()

    if P1_AI and P2_AI:
        possibleMoves = []
        imagecounter = 0
        while True:
            temp = state.evaluate(True)
            if temp == None:
                AVERAGEGAMELENGTH += len(possibleMoves)
                AVERAGEMOVES += sum(possibleMoves) / len(possibleMoves)
                GAMESPLAYED += 1
                return reset(windowSurface, "GAME OVER", l, b)
            state = updatestateTree(state, temp.board)
            possibleMoves.append(len(state.children))

            b = state.board

    while True:
        clock.tick(FRAME_RATE)  # throttle cpu
        windowSurface.fill(BACKGROUND_COLOR)
        pos = pygame.mouse.get_pos()
        current = pixelToHex(l, Point(pos[0], pos[1]))
        drawBoard(windowSurface, BACKGROUND_COLOR, BOARD_COLOR, l, b)

        # Draw held piece
        if selected != None:
            if holdingPiece:
                pygame.draw.circle(windowSurface, selectedColor, pos, int(l.size[0] / 2))
            else:
                drawHex(windowSurface, selectedColor, l, pixelToHex(l, Point(pos[0], pos[1]), False))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if current in b:
                    if not movedHex and hexPickup(b, current, turn, movedPiece or captured, pieces):
                        selected = current
                        selectedColor = (BOARD_COLOR, tuple([min(i + 40, 255) for i in BOARD_COLOR]), tuple([max(i - 40, 0) for i in BOARD_COLOR]))[sign(b[current] + 1)]
                    elif not movedPiece and piecePickup(b, current, turn):
                        selected = current
                        selectedColor = tuple([(None, 0, 255)[turn]] * 3)
                        holdingPiece = True
                    else:
                        # failed pickup
                        pass
            elif event.type == pygame.MOUSEBUTTONUP:
                if selected != None:  # dropping a piece
                    if holdingPiece:
                        movedPiece = piecePlace(b, Move(selected, current), turn)
                        if movedPiece:
                            removePiece(selected, pieces)
                            pieces[(turn + 1) / 2].append(current)
                        if hasWon(pieces) != 0:
                            return reset(windowSurface, "GAME OVER", l, b)
                    else:
                        movedHex = hexPlace(b, Move(selected, current), turn, movedPiece or captured, pieces)
                elif not captured and current in underAttack:  # capturing a piece
                    b[current] += turn
                    captured = True
                    removePiece(current, pieces)
                    if hasWon(pieces) != 0:
                        return reset(windowSurface, "GAME OVER", l, b)
                temp = movedHex + movedPiece + captured
                if temp == 1 and len(currentMove) == 0 or temp == 2:
                    if captured:
                        currentMove.append(current)
                    else:
                        currentMove.append(Move(selected, current))
                if temp == 2:
                    movedHex = False
                    movedPiece = False
                    captured = False
                    turn = -turn
                    # state = updatestateTree(state, b)
                    # if turn == -1 and P2_AI or turn == 1 and P1_AI:
                    #     print state
                    #     state = updatestateTree(state, state.evaluate(True).board)
                    #     pieces = getPieces(state.board)
                    #     b = state.board
                    #     turn = -turn
                    currentMove = []
                    underAttack = getThreatened(turn, pieces)
                    print "Black's" if turn == 1 else "White's",
                    print "Turn"
                selected = None
                holdingPiece = False
            elif event.type == pygame.QUIT:
                return False

if __name__ == '__main__':
    pygame.init()
    random.seed()
    windowSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Hexagonal Iso-Path')
    while main():
        pass
    print AVERAGEGAMELENGTH / GAMESPLAYED, GAMESPLAYED, AVERAGEMOVES / GAMESPLAYED
    pygame.quit()
    sys.exit()
