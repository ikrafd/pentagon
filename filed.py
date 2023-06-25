from setting import *
from pentamino import Pentamino, BacktrackingSolver


class Field:
    def __init__(self, app):
        self.solveComplete = False
        self.backTrack = None
        self.app = app
        self.spriteGroup = pg.sprite.Group()
        self.pentamino = Pentamino(self)
        self.array = [[0] * numberOfCells for _ in range(numberOfCells)]
        self.reserveArray = [[0] * numberOfCells for _ in range(numberOfCells)]

    def drawFiled(self):
        for a in range(0, numberOfCells):
            for b in range(0, numberOfCells):
                color = fieldColor
                if self.array[b][a] == 1:
                    color = "black"
                elif self.array[b][a] == -2:
                    color = self.pentamino.blocksS[0].color
                pg.draw.rect(self.app.screen, color,
                             (a * sizeSquare + startX, b * sizeSquare + startY, sizeSquare, sizeSquare), 0)

        for i in range(numberOfCells + 2):
            if i == 0 or i == numberOfCells:  # First and last cells
                pg.draw.line(self.app.screen, 'black', (startX + sizeSquare * i, startY),
                             (startX + sizeSquare * i, endY), 4)
            elif i != 13:
                pg.draw.line(self.app.screen, 'black', (startX + sizeSquare * i, startY),
                             (startX + sizeSquare * i, endY), 2)
            else:
                pg.draw.line(self.app.screen, 'black', (startX + sizeSquare * i, startY),
                             (startX + sizeSquare * i, endY - sizeSquare), 2)

        # Draw horizontal lines
        for i in range(numberOfCells + 2):
            if i == 0 or i == numberOfCells:  # First and last cells
                pg.draw.line(self.app.screen, 'black', (startX, startY + sizeSquare * i),
                             (endX, startY + sizeSquare * i), 4)
            elif i != 13:
                pg.draw.line(self.app.screen, 'black', (startX, startY + sizeSquare * i),
                             (endX, startY + sizeSquare * i), 2)
            else:
                pg.draw.line(self.app.screen, 'black', (startX, startY + sizeSquare * i),
                             (endX - sizeSquare, startY + sizeSquare * i), 2)

            # Draw numbers
            occupiedRow, occupiedColumn = self.calculateOccupiedCells()

            font_size = 20
            font = pg.freetype.SysFont(None, font_size)
            x = startX
            y = startY + sizeSquare * numberOfCells + sizeSquare // 2

            for column in occupiedColumn:
                number_text = font.render(str(column), fgcolor="black")[0]
                text_rect = number_text.get_rect(center=(x + sizeSquare // 2, y))
                self.app.screen.blit(number_text, text_rect)
                x += sizeSquare

            x = startX + sizeSquare * numberOfCells + sizeSquare // 2
            y = startY
            for row in occupiedRow:
                number_text = font.render(str(row), fgcolor="black")[0]
                text_rect = number_text.get_rect(center=(x, y + sizeSquare // 2))
                self.app.screen.blit(number_text, text_rect)
                y += sizeSquare

    def generateFiled(self):
        self.app.lastClickTime = pg.time.get_ticks()
        self.newGame()
        pentaminoes = changeSet()

        self.backTrack = BacktrackingSolver(self, pentaminoes)
        self.solveComplete = False

        while self.backTrack.trying < 100 and not self.solveComplete:
            self.solveComplete = self.backTrack.solve()
            self.backTrack.trying += 1
            self.backTrack.nextIndex = 0
            self.backTrack.shapes = changeSet()

        count = 0
        while count < 19:
            row = random.randint(0, numberOfCells - 1)
            column = random.randint(0, numberOfCells - 1)
            if self.array[row][column] != -2 and self.checkAdjacentEmpty(row, column):
                self.array[row][column] = 1
                count += 1

        self.reserveArray = copy.deepcopy(self.array)

        for i in range(numberOfCells):
            for j in range(numberOfCells):
                if self.array[i][j] == -1 or self.array[i][j] == -2:
                    self.array[i][j] = 0

    def checkAdjacentEmpty(self, row, column):
        for i in range(max(0, row - 1), min(row + 2, numberOfCells)):
            for j in range(max(0, column - 1), min(column + 2, numberOfCells)):
                if self.array[i][j] == 1:
                    return False
        return True

    def update(self):
        self.pentamino.update()
        self.spriteGroup.update()

    def draw(self):
        self.drawFiled()
        self.spriteGroup.draw(self.app.screen)

    def calculateOccupiedCells(self):
        row_counts = [0] * 12
        col_counts = [0] * 12

        for i in range(12):
            for j in range(12):
                if self.array[i][j] == -2:
                    row_counts[i] += 1
                    col_counts[j] += 1

        return row_counts, col_counts

    def checkSolution(self):
        count = 0
        row_counts = self.calculateOccupiedCells()[0]
        for i in range(12):
            if row_counts[i] != 0:
                count += row_counts[i]

        for block in self.pentamino.blocksS:
            row = int(block.pos[1] - y)
            column = int(block.pos[0] - x + 2)
            neighbors = [(row - 1, column), (row + 1, column), (row, column - 1), (row, column + 1),
                         (row - 1, column - 1), (row - 1, column + 1), (row + 1, column - 1),
                         (row + 1, column + 1)]
            for neighbor_row, neighbor_column in neighbors:
                if 0 <= neighbor_row < 12 and 0 <= neighbor_column < 12:
                    if self.array[neighbor_row][neighbor_column] == -2 and self.findShape(neighbor_row,
                                                                                          neighbor_column) != block.shape and self.findShape(
                        neighbor_row, neighbor_column) is not None:
                        shape = self.findShape(neighbor_row, neighbor_column)
                        pymsgbox.alert(f"Розв'язок невірний, фігури {block.shape} та {shape} дотикаються", "Розв'язок")
                        return
        if count != 60:
            pymsgbox.alert("Не всі фігури розміщено", "Розв'язок")
            return
        pymsgbox.alert("Головоломка розв'язана, будь ласка, розпочніть знову", "Розв'язок")
        return

    def findShape(self, row, column):
        for block in self.pentamino.blocksS:
            rowBlock = int(block.pos[1] - y)
            columnBlock = int(block.pos[0] - x + 2)
            if 0 <= rowBlock < 12 and 0 <= columnBlock < 12:
                if row == rowBlock and column == columnBlock:
                    return block.shape

    def autoSolve(self):
        self.array = self.reserveArray
        self.pentamino.placeShape()

    def save(self):
        filename = "solution.txt"

        with open(filename, 'w') as file:
            for row in self.array:
                file.write(' '.join(map(str, row)) + '\n')
        pymsgbox.alert("Збережено", "Збереження")

    def newGame(self):
        self.array = [[0 for _ in range(12)] for _ in range(12)]
        for block in self.pentamino.blocksS:
            block.pos = block.firstPos
        for block in self.pentamino.blocksF:
            block.pos = block.firstPos


class Button:
    def __init__(self, color, x, y, text='', action=None):
        self.color = color
        self.hoverColor = (200, 200, 200)
        self.x = x
        self.y = y
        self.width = 190
        self.height = 35
        self.radius = 5
        self.text = text
        self.action = action

    def draw(self, win, pos, outline=None):

        if self.isOver(pos):
            color = self.hoverColor
        else:
            color = self.color

        if outline:
            pg.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4),
                         border_radius=self.radius)

        pg.draw.rect(win, color, (self.x, self.y, self.width, self.height), border_radius=self.radius)

        if self.text != '':
            font = pg.font.SysFont('tahoma', 30)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text,
                     (self.x + (self.width / 2 - text.get_width() / 2),
                      self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False

    def performAction(self):
        if self.action:
            self.action()
