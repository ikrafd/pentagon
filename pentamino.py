from setting import *

class Block(pg.sprite.Sprite):
    def __init__(self, pentamino, pos, offset, shape):
        self.pentamino = pentamino
        self.pos = pos

        self.offset = offset
        self.shape = shape

        self.startPos = pos
        self.firstPos = pos

        self.clicked = False
        super().__init__(pentamino.field.spriteGroup)
        self.image = pg.Surface([sizeSquare, sizeSquare])
        self.color = (229, 190, 236)
        self.image.fill((229, 190, 236))

        self.rect = self.image.get_rect()
        self.rect.topleft = (abs(self.pos[0]) * sizeSquare, -self.pos[1] * sizeSquare)

    def rotate(self, pivotPos):
        translated = self.pos - pivotPos
        rotated = translated.rotate(90)
        return rotated + pivotPos

    def move(self, offset):
        new_pos = (self.pos[0] + offset[0], self.pos[1] + offset[1])
        if 0 <= new_pos[0] < fieldWidth - sizeSquare and 0 <= new_pos[1] < fieldHeight - sizeSquare:
            self.rect.topleft = pg.mouse.get_pos()
            self.pos = vec(new_pos)


class Pentamino:
    def __init__(self, Field):
        self.field = Field
        self.shapes = []
        self.pos = vec(x + 13, y + 2)
        self.blocksF = self.initBlocksField()
        self.blocksS = self.initBlocksShape()
        self.inside = False

    def initBlocksField(self):
        blocks = []
        i = 0
        j = 0
        self.shapes.extend(list(pentaminoesF.keys()))
        for shape in pentaminoesF.keys():
            offsetShape = vec(self.pos[0] + i * 6 + pentaminoStart[shape][0],
                              self.pos[1] + j * 6 + pentaminoStart[shape][1])
            shapeBlock = [Block(self, vec(pos[0], pos[1]) + offsetShape, offsetShape, shape) for pos in
                          pentaminoesF[shape]]
            blocks.extend(shapeBlock)
            i += 1
            if i >= 4 or i >= 8:
                j += 1
                i = 0

        return blocks

    def initBlocksShape(self):
        blocks = []
        i = 0
        j = 0
        self.shapes.extend(list(pentaminoesShape.keys()))
        for shape in pentaminoesShape.keys():
            offsetShape = vec(self.pos[0] + i * 6 + pentaminoStart[shape][0],
                              self.pos[1] + j * 6 + pentaminoStart[shape][1])
            shapeBlock = [Block(self, vec(pos[0], pos[1]) + offsetShape, offsetShape, shape) for pos in
                          pentaminoesShape[shape]]
            blocks.extend(shapeBlock)
            i += 1
            if i >= 4 or i >= 8:
                j += 1
                i = 0

        return blocks

    def changeColor(self):
        rgb = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        if rgb != fieldColor:
            for block in self.blocksS:
                block.image.fill(rgb)
                block.color = rgb

    def update(self):
        for block in self.blocksS:
            block.rect.topleft = (abs(block.pos[0]) * sizeSquare, block.pos[1] * sizeSquare)

    def isInside(self, targetShape):
        for block in self.blocksS:
            if block.shape == targetShape:
                isInsideBounds = startX <= block.rect.x <= endX and startY - 80 <= block.rect.y <= endY
                if not isInsideBounds:
                    if self.inside:
                        self.removeShape(targetShape)
                        self.inside = False
                    return False
        self.inside = True
        return True

    def rotate(self, shape):
        blocksToRotate = [block for block in self.blocksS if block.shape == shape]
        if blocksToRotate:
            pivotPos = blocksToRotate[0].pos
            for block in blocksToRotate:
                newPosition = block.rotate(pivotPos)
                block.pos = newPosition

    def tryPlaceShape(self, targetShape):
        newPos = []
        occupied = False
        for block in self.blocksS:
            if block.shape == targetShape:
                row = int(block.pos[0] - x + 2)
                column = int(block.pos[1] - y)
                if 0 > row or row > 11 or 0 > column or column > 11:
                    return False
                if (self.field.array[column][row] != 1
                        and self.field.array[column][row] != -2
                        and self.field.array[column][row] != -1):
                    newPos.append([row, column])
                else:
                    occupied = True
                    return False

        if not occupied:
            if self.checkCollision(newPos):
                return False

            self.fillField(newPos)
            return True

    def checkCollision(self, pos):
        for row, column in pos:
            if self.field.array[column][row] == -2 and self.blocksS:
                return True
        return False

    def fillField(self, pos):
        print(type(pos))
        for row, column in pos:
            self.field.array[column][row] = -2

    def move(self, shape, offset):
        print(type(shape), type(offset))
        blocks_to_move = [block for block in self.blocksS if block.shape == shape]
        if blocks_to_move:
            for block in blocks_to_move:
                new_pos = (block.pos[0] + offset[0], block.pos[1] + offset[1])
                if not (0 <= new_pos[0] < fieldWidth // sizeSquare and fieldHeight // sizeSquare > new_pos[1] >= 0):
                    return
            for block in blocks_to_move:
                block.move(offset)

    def backShape(self, targetShape):
        for block in self.blocksS:
            if block.shape == targetShape:
                block.pos = block.startPos

    def removeShape(self, targetShape):
        for block in self.blocksS:
            if block.shape == targetShape:
                row = int(block.startPos[0] - x + 2)
                column = int(block.startPos[1] - y)
                if 0 <= row <= 11 and 0 <= column <= 11 and self.field.array[column][row] == -2:
                    self.field.array[column][row] = 0

    def updateStartPos(self, targetShape):
        for block in self.blocksS:
            if block.shape == targetShape:
                block.startPos = block.pos

    def placeShape(self):
        for block in self.blocksS:
            block.pos = (-10, -10)


class BacktrackingSolver:
    def __init__(self, Field, shapes):
        self.field = Field
        self.useShape = set()
        self.useShapeCor = set()
        self.nextIndex = 0
        self.nextShape = 0
        self.shapes = shapes
        self.cache = []
        self.trying = 1

    def solve(self):
        if pg.time.get_ticks() - self.field.app.lastClickTime > 4000 * self.trying:
            return False
        if self.isSolutionComplete():
            print(pg.time.get_ticks())
            return True
        shape = self.getNextPentamino()
        if shape is not None:
            positions = self.getValidPositions(shape)
            if len(positions) > 0:
                for position in positions:
                    self.placePentamino(shape, position)
                    if self.solve():
                        return True
                    self.removePentamino(shape, position)
            else:
                return False
        return False

    def isSolutionComplete(self):
        return len(self.useShape) == 12

    def getNextPentamino(self):
        while self.nextIndex < len(pentaminoesF):
            nextPentamino = list(self.shapes.keys())[self.nextIndex]
            if nextPentamino not in self.useShape:
                if self.nextIndex < 12:
                    self.nextIndex += 1
                return self.shapes[nextPentamino]
            else:
                self.nextIndex += 1
        return None

    def getValidPositions(self, pentamino):
        rowStart, rowEnd, colStart, colEnd = 0, 0, 0, 0
        possiblePositions = []
        countZeros = sum(row.count(0) for row in self.field.array)
        if countZeros < (12 - self.nextIndex) * 5:
            return possiblePositions

        if len(self.useShape) < 5:
            rowEnd = 7
            colEnd = 12
        elif len(self.useShape) < 13:
            rowEnd = 12
            colEnd = 12

        for row in range(rowStart, rowEnd):
            for column in range(colStart, colEnd):
                temp = self.calculatePosition(pentamino, row, column)
                if len(temp) > 0:
                    possiblePositions.extend(temp)

        if len(possiblePositions) != 0:
            if len(possiblePositions) == 1:
                self.cache.append(possiblePositions)
            return possiblePositions
        else:
            return []

    def calculatePosition(self, pentamino, row, column):
        possiblePositions = []
        if self.checkPentaminoFit(pentamino, row, column):
            figure = [(pos[0] + row, pos[1] + column) for pos in pentamino]
            if self.checkFigureWithinBounds(figure):
                possiblePositions.append(figure)
            for rotation in range(1, 4):
                rotatedFigure = [(-pos[1], pos[0]) for pos in figure]
                if self.checkPentaminoFit(rotatedFigure, row, column):
                    rotatedFigure = [(pos[0] + row, pos[1] + column) for pos in rotatedFigure]
                    if self.checkFigureWithinBounds(rotatedFigure):
                        possiblePositions.append(rotatedFigure)
                figure = rotatedFigure
        return possiblePositions

    def checkFigureWithinBounds(self, figure):
        return all(0 <= pos[0] < numberOfCells and 0 <= pos[1] < numberOfCells for pos in figure)

    def placePentamino(self, pentamino, position):
        beforeLen = len(self.useShape)
        self.useShape.add(tuple(pentamino))
        afterLen = len(self.useShape)

        if afterLen > beforeLen:
            if self.isUniquePosition(position):
                self.useShapeCor.add(tuple(position))
                for row, column in position:
                    self.field.array[row][column] = -2

                for row, column in position:
                    neighbors = [(row - 1, column), (row + 1, column), (row, column - 1), (row, column + 1),
                                 (row - 1, column - 1), (row - 1, column + 1), (row + 1, column - 1),
                                 (row + 1, column + 1)]
                    for neighbor_row, neighbor_column in neighbors:
                        if 0 <= neighbor_row < len(self.field.array) and 0 <= neighbor_column < len(
                                self.field.array[0]):
                            if self.field.array[neighbor_row][neighbor_column] == 0:
                                self.field.array[neighbor_row][neighbor_column] = -1
            else:
                self.useShape.remove(tuple(pentamino))
        else:
            self.useShape.remove(tuple(pentamino))

    def removePentamino(self, pentamino, position):
        beforeLen = len(self.useShape)
        self.useShape.remove(tuple(pentamino))
        afterLen = len(self.useShape)

        if afterLen < beforeLen:
            for row, column in position:
                self.field.array[row][column] = 0

            for row, column in position:
                neighbors = [(row - 1, column), (row + 1, column), (row, column - 1), (row, column + 1),
                             (row - 1, column - 1), (row - 1, column + 1), (row + 1, column - 1),
                             (row + 1, column + 1)]
                for neighborRow, neighborColumn in neighbors:
                    if 0 <= neighborRow < len(self.field.array) and 0 <= neighborColumn < len(self.field.array[0]):
                        if self.field.array[neighborRow][neighborColumn] == -1:
                            if not self.checkContourConnected(neighborRow, neighborColumn):
                                self.field.array[neighborRow][neighborColumn] = 0
        if position in self.cache:
            self.cache.remove(position)
        self.useShapeCor.remove(tuple(position))
        self.nextIndex -= 1

    def checkContourConnected(self, row, column):
        secondNeighbors = [(row - 1, column), (row + 1, column), (row, column - 1), (row, column + 1),
                            (row - 1, column - 1), (row - 1, column + 1), (row + 1, column - 1),
                            (row + 1, column + 1)]
        for secondRow, secondColumn in secondNeighbors:
            if 0 <= secondRow < len(self.field.array) and 0 <= secondColumn < len(self.field.array[0]):
                if self.field.array[secondRow][secondColumn] == -2:
                    return True
        return False


    def checkPentaminoFit(self, pentamino, row, column):
        adjusted_shape = [(pos[0] + row, pos[1] + column) for pos in pentamino]
        if any(
                pos[0] < 0 or pos[0] >= numberOfCells or pos[1] < 0 or pos[1] >= numberOfCells
                or self.field.array[pos[0]][pos[1]] == -2 or self.field.array[pos[0]][pos[1]] == -1 or
                self.field.array[pos[0]][pos[1]] == 1
                for pos in adjusted_shape
        ):
            return False
        return True

    def isUniquePosition(self, figure):
        for pos in figure:
            if pos in self.useShapeCor:
                return False
        return True
