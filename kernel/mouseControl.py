import pygame


class MouseControl:
    def __init__(self, gameScreen):
        self.gameScreen = gameScreen
        self.mousePos = (0, 0)
        self.mouseDown = False

    def update(self):
        self.mousePos = pygame.mouse.get_pos()
        self.mouseDown = pygame.mouse.get_pressed()[0]

    def getPos(self):
        return self.mousePos

    def isMouseDown(self):
        return self.mouseDown

    def isPointInRect(self, point, rect):
        return rect.collidepoint(point)
