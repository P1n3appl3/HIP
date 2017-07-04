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
    color = (hexColor, tuple([min(i + 60, 255) for i in hexColor]), tuple([max(i - 60, 0) for i in hexColor]))
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
bgColor = (0,255,255)
boardColor = (0,128,0)

while True:
    windowSurface.fill(bgColor)
    pos = pygame.mouse.get_pos()
    current = pixelToHex(l, Point(pos[0], pos[1]))
    drawBoard(windowSurface, bgColor, boardColor, l, b)
    if selected != None:
        drawHex(windowSurface, selectedColor, l, pixelToHex(l, Point(pos[0], pos[1]), False))
    # drawHex(windowSurface, (145, 170, 100), l, current)
    # for h in hexNeighbors(current, boardSize):
    #     if b[h] == 0:
    #         drawHex(windowSurface, (230, 170, 100), l, h)
    # for h in b:
    #     # print coords
    #     #textsurface = font.render(', '.join([str(i) for i in h]), False, (255, 255, 255))
    #     textsurface = font.render(str(b[h]), False, (255, 255, 255))
    #     textPos = hexToPixel(l, h)
    #     textSize = textsurface.get_rect()
    #     windowSurface.blit(textsurface, (textPos.x - textSize.width / 2, textPos.y - textSize.height / 2))


    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if current in b:
                if b[current] == 0 or b[current] == turn:
                    selected = current
                    selectedColor = (boardColor, tuple([min(i + 60, 255) for i in boardColor]), tuple([max(i - 60, 0) for i in boardColor]))[sign(b[current])]
                    b[selected] -= 1
                elif sign(b[current]) == turn:
                    pass #pick up piece
            print "click", selected
        elif event.type == pygame.MOUSEBUTTONUP:
            if selected != None:
                if -2 < b[current] < 1: #move is valid
                    b[current] += 1
                else:
                    b[selected] += 1
                selected = None
            print "release"
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
