import pygame
import random
from src.game import *


def drawHex(surface, color, layout, hex, width=0):
    x, y = tuple(hexToPixel(layout, hex))
    if width == 0:
        pygame.draw.polygon(surface, color, polygonCorners(layout, hex))
    else:
        pygame.draw.aalines(surface, color, width, polygonCorners(layout, hex))


def drawBoard(surface, outlineColor, hexColor, layout, board):
    color = (hexColor, tuple([min(i + 40, 255) for i in hexColor]), tuple([max(i - 40, 0) for i in hexColor]))
    for h in board:
        drawHex(surface, color[sign(board[h])], layout, h)
        if abs(board[h]) == 2:
            c = (None, 0, 255)[sign(board[h])]
            temp = hexToPixel(layout, h)
            pygame.draw.circle(surface, (c, c, c), (int(temp.x), int(temp.y)), int(layout.size[0] / 2))
    for h in board:
        drawHex(surface, outlineColor, layout, h, 2)

def reset(surface, text, layout, board):
    words = pygame.font.SysFont(FONT, FONT_SIZE).render(text, 0, TEXT_COLOR)
    while True:
        windowSurface.fill(BACKGROUND_COLOR)
        drawBoard(windowSurface, BACKGROUND_COLOR, BOARD_COLOR, layout, board)
        surface.blit(words, (SCREEN_WIDTH / 2 - words.get_width() / 2, SCREEN_HEIGHT / 2 - words.get_height() / 2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                return True
            elif event.type == pygame.QUIT:
                return False

def main():
    l = Layout(Orientation(math.sqrt(3.0), math.sqrt(3.0) / 2.0, 0.0, 3.0 / 2.0, math.sqrt(3.0) / 3.0, -1.0 / 3.0, 0.0, 2.0 / 3.0, 0.5), Point(HEX_SIZE, HEX_SIZE), Point(SCREEN_WIDTH / 2., SCREEN_HEIGHT / 2.))
    b = createBoard()
    turn = 1
    movedHex = False
    movedPiece = False
    captured = False
    selected = None
    underAttack = []
    selectedColor = None
    holdingPiece = False

    while True:
        windowSurface.fill(BACKGROUND_COLOR)
        pos = pygame.mouse.get_pos()
        current = pixelToHex(l, Point(pos[0], pos[1]))
        drawBoard(windowSurface, BACKGROUND_COLOR, BOARD_COLOR, l, b)

        if selected == None:
            if SHOW_LEGAL_MOVE_HINTS:
                pass
        else:
            if holdingPiece:
                pygame.draw.circle(windowSurface, selectedColor, pos, int(l.size[0] / 2))
            else:
                drawHex(windowSurface, selectedColor, l, pixelToHex(l, Point(pos[0], pos[1]), False))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if current in b:
                    if not movedHex and hexPickup(b, current, turn, movedPiece or captured):
                        selected = current
                        selectedColor = (BOARD_COLOR, tuple([min(i + 60, 255) for i in BOARD_COLOR]), tuple([max(i - 60, 0) for i in BOARD_COLOR]))[sign(b[current] + 1)]
                    elif not movedPiece and piecePickup(b, current, turn):
                        selected = current
                        selectedColor = tuple([(None, 0, 255)[turn]] * 3)
                        holdingPiece = True
                    elif not captured and current in underAttack:
                        b[current] += turn
                        captured = True
                        if hasWon(b, turn):
                            return reset(windowSurface, "VICTORY", l, b)
                    else:
                        print "invalid pickup"
            elif event.type == pygame.MOUSEBUTTONUP:
                if selected != None:
                    if holdingPiece:
                        movedPiece = piecePlace(b, Move(selected, current), turn)
                        if hasWon(b, turn):
                            return reset(windowSurface, "VICTORY", l, b)
                    else:
                        movedHex = hexPlace(b, Move(selected, current), turn, movedPiece or captured)
                selected = None
                holdingPiece = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                return False

            if movedHex + movedPiece + captured == 2:
                movedHex = False
                movedPiece = False
                captured = False
                turn = -turn
                underAttack = getThreatened(b, turn)
                print "switch turn"


if __name__ == '__main__':
    pygame.init()
    windowSurface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption('Hexagonal Iso-Path')
    while main():
        pass
    sys.exit()
