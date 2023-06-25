import pygame as pg
import pymsgbox
import random
import copy
import sys



vec = pg.math.Vector2
fieldColor = (42, 47, 79)
pg.font.init()
font = pg.font.SysFont("Arial", 30, 1, 1)

sizeSquare = 40
numberOfCells = 12
fieldSize = fieldWidth, fieldHeight = 1500, 800
coordinateOfField = x, y = 3.10, 1

startX = x + sizeSquare
endX = x + sizeSquare + sizeSquare * (numberOfCells+1)
startY = y + sizeSquare
endY = y + sizeSquare + sizeSquare * (numberOfCells+1)


def changeSet():
    global pentaminoesF
    shapes = list(pentaminoesF.keys())
    random.shuffle(shapes)

    # Create a new dictionary with shuffled order of shapes
    pentaminoesF_shuffled = {shape: pentaminoesF[shape] for shape in shapes}

    # Assign the shuffled dictionary back to the global variable
    pentaminoesF = pentaminoesF_shuffled
    return pentaminoesF
#field
pentaminoesF = {
    'P': [(0, 0), (0, -1), (1, -1), (1, 0), (-1, -1)],
    'T': [(0, 0), (-1, -1), (0, 1), (0, -1), (1, -1)],
    'V': [(-1, 0), (-1, -1), (-1, 1), (0, -1), (1, -1)],
    'W': [(-1, 0), (-1, -1), (0, -1), (0, -2), (-2, 0)],
    'I': [(0, 0), (0, -1), (0, -2), (0, -3), (0, 1)],
    'U': [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0)],
    'Z': [(0, 0), (0, -1), (0, -2), (-1, -2), (1, 0)],
    'L': [(0, 0), (-1, 0), (0, -1), (0, -2), (0, -3)],
    'F': [(0, 0), (0, -1), (-1, -1), (0, -2), (1, -2)],
    'Y': [(0, 0), (0, -1), (0, -2), (0, -3), (1, -2)],
    'N': [(0, 0), (0, -1), (0, 1), (-1, 2), (-1, 1)],
    'X': [(0, 0), (0, -1), (0, -2), (1, -1), (-1, -1)]
}



#big
pentaminoesShape= {
    'P': [(0, 0), (0, -1), (1, -1), (1, 0), (-1, 0)],
    'T': [(0, 0), (-1, -1), (0, 1), (0, -1), (1, -1)],
    'V': [(0, 0), (0, -1), (0, 1), (1, -1), (2, -1)],
    'W': [(0, 0), (0, -1), (1, -1), (1, -2), (-1, 0)],
    'I': [(0, 0), (0, -1), (0, -2), (0, -3), (0, 1)],
    'U': [(0, 0), (0, -1), (1, -1), (2, -1), (2, 0)],
    'L': [(0, 0), (1, 0), (0, -1), (0, -2), (0, -3)],
    'Z': [(0, 0), (0, -1), (0, -2), (1, -2), (-1, 0)],
    'F': [(0, 0), (0, -1), (1, -1), (0, -2), (-1, -2)],
    'Y': [(0, 0), (0, -1), (0, -2), (0, -3), (-1, -2)],
    'N': [(0, 0), (0, -1), (0, 1), (-1, -2), (-1, -1)],
    'X': [(0, 0), (0, -1), (0, -2), (1, -1), (-1, -1)]
}

pentaminoStart = {
    'P': (0, 0),
    'T': (0, 0),
    'V': (0, 0),
    'W': (0, 0),
    'I': (0, 0),
    'U': (0, 0),
    'Z': (0, 0),
    'L': (0, 0),
    'F': (0, 0),
    'Y': (0, 0),
    'N': (0, 0),
    'X': (0, 0)
}