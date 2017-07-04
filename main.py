import pygame
import random
import sys
from lib.engine import *


def drawHex(surface, color, layout, hex, width=0):
    x, y = tuple(hexToPixel(layout, hex))
    if width == 0:
        pygame.draw.polygon(surface, color, polygonCorners(layout, hex))
    else:
        pygame.draw.aalines(surface, color, width, polygonCorners(layout, hex))

def drawBoard(surface, outlineColor, hexColor, layout, board):
    color = (hexColor, tuple([min(i + 60, 255) for i in hexColor]), tuple([max(i - 40, 0) for i in hexColor]))
    for h in board:
        drawHex(surface, color[sign(board[h])], layout, h)
        if abs(board[h]) == 2:
            c = (None, 0, 255)[sign(board[h])]
            temp = hexToPixel(layout, h)
            pygame.draw.circle(surface, (c, c, c), (int(temp.x), int(temp.y)), int(layout.size[0]/2))
    for h in board:
        drawHex(surface, outlineColor, layout, h, 2)

pygame.init()
hexSize = 40
screenSize = Point(500, 500)

windowSurface = pygame.display.set_mode(tuple(screenSize), pygame.RESIZABLE)

pygame.display.set_caption('Hexagonal Iso-Path')

font = pygame.font.SysFont('Cambria', 20)

l = Layout(Orientation(math.sqrt(3.0), math.sqrt(3.0) / 2.0, 0.0, 3.0 / 2.0, math.sqrt(3.0) / 3.0, -1.0 / 3.0, 0.0, 2.0 / 3.0, 0.5), Point(hexSize, hexSize), Point(screenSize.x / 2., screenSize.y / 2.))

boardSize = 3
b = createHexBoard(boardSize)
turn = 1
selected = None
selectedColor = None
holdingPiece = False
bgColor = (60, 71, 77)
boardColor = (64,128,172)

while True:
    windowSurface.fill(bgColor)

    pos = pygame.mouse.get_pos()
    current = pixelToHex(l, Point(pos[0], pos[1]))
    drawBoard(windowSurface, bgColor, boardColor, l, b)
    if selected != None:
        if holdingPiece:
            c = (None, 0, 255)[sign(b[selected])]
            pygame.draw.circle(windowSurface, (c, c, c), pos, int(l.size[0]/2))
        else:
            drawHex(windowSurface, selectedColor, l, pixelToHex(l, Point(pos[0], pos[1]), False))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if current in b:
                if b[current] == 0 or b[current] == turn:
                    selected = current
                    selectedColor = (boardColor, tuple([min(i + 60, 255) for i in boardColor]), tuple([max(i - 60, 0) for i in boardColor]))[sign(b[current])]
                    b[selected] -= 1
                elif sign(b[current]) == turn:
                    selected = current
                    b[current] -= sign(b[current])
                    holdingPiece = True
                    print "pick up piece"
            print "click", selected
        elif event.type == pygame.MOUSEBUTTONUP:
            if selected != None:
                if holdingPiece:
                    if current in hexNeighbors(selected, boardSize) and sign(b[selected]) == b[current]:
                        b[current] += sign(selected)
                        print "place piece"
                    else:
                        b[selected] += sign(selected)
                else:
                    if current in b and -2 < b[current] < 1: #move is valid
                        b[current] += 1
                    else:
                        b[selected] += 1
            selected = None
            holdingPiece = False
            print "release"
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
