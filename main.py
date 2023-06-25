from setting import *
from filed import Field, Button

class App:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Pentagon")
        self.screen = pg.display.set_mode(fieldSize)
        self.clock = pg.time.Clock()

        self.field = Field(self)
        self.buttons = [Button((92, 79, 156), 60, 590, 'Generate', action=self.field.generateFiled),
                        Button((92, 79, 156), 310, 590,  'Check', action=self.field.checkSolution),
                        Button((145, 127, 179), 190, 640,  'Auto solve', action=self.field.autoSolve),
                        Button((92, 79, 156), 60, 690, 'Save', action=self.field.save),
                        Button((92, 79, 156), 190, 740, 'New Game', action=self.field.newGame),
                        Button((92, 79, 156), 310, 690,  'Change color', action=self.field.pentamino.changeColor)]
        self.lastClickTime = 0

    def draw(self):
        self.screen.fill(color=fieldColor)

        self.field.draw()
        pos = pg.mouse.get_pos()

        for button in self.buttons:
            button.draw(self.screen, pos)
        pg.display.flip()

    def checkEvents(self):
        doubleClickTime = 200
        for event in pg.event.get():

            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    currentTime = pg.time.get_ticks()
                    elapsedTime = currentTime - self.lastClickTime
                    if elapsedTime < doubleClickTime:
                        mx, my = pg.mouse.get_pos()
                        for block in self.field.pentamino.blocksS:
                            if block.rect.collidepoint(mx, my):
                                self.field.pentamino.rotate(block.shape)
                                self.field.pentamino.removeShape(block.shape)

                    else:
                        self.lastClickTime = currentTime
                        for sprite in self.field.pentamino.blocksS:
                            if sprite.rect.collidepoint(event.pos):
                                self.field.pentamino.updateStartPos(sprite.shape)
                                self.field.pentamino.removeShape(sprite.shape)
                                sprite.clicked = True

            elif event.type == pg.MOUSEMOTION:
                for sprite in self.field.pentamino.blocksS:
                    if sprite.clicked:
                        relX, relY = sprite.rect[0], sprite.rect[1]
                        diffX = pg.mouse.get_pos()[0] - relX
                        diffY = pg.mouse.get_pos()[1] - relY

                        if diffX % 40 == 0:
                            self.field.pentamino.move(sprite.shape, (int(diffX // 40), 0))
                        elif diffY % 40 == 0:
                            self.field.pentamino.move(sprite.shape, (0, int(diffY // 40)))

            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    for sprite in self.field.pentamino.blocksS:
                        if sprite.clicked:
                            if self.field.pentamino.isInside(sprite.shape):
                                if not self.field.pentamino.tryPlaceShape(sprite.shape):
                                    self.field.pentamino.backShape(sprite.shape)
                            sprite.clicked = False

            for button in self.buttons:
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    if button.isOver(event.pos):
                        button.performAction()

    def run(self):
        while True:
            self.checkEvents()
            self.field.update()
            self.draw()


if __name__ == '__main__':
    app = App()
    app.run()
