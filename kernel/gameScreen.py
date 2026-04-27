import pygame


class GameScreen:
    WIDTH = 480
    HEIGHT = 720
    FPS = 60

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("雷电 - 纵卷轴射击游戏")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 24)
        self.bigFont = pygame.font.SysFont("arial", 48)

    def fillBackground(self, color=(0, 0, 20)):
        self.screen.fill(color)

    def updateDisplay(self):
        pygame.display.flip()

    def tick(self):
        return self.clock.tick(self.FPS)

    def getScreen(self):
        return self.screen

    def getWidth(self):
        return self.WIDTH

    def getHeight(self):
        return self.HEIGHT

    def drawText(self, text, x, y, color=(255, 255, 255), font=None):
        if font is None:
            font = self.font
        textSurface = font.render(text, True, color)
        textRect = textSurface.get_rect()
        textRect.centerx = x
        textRect.top = y
        self.screen.blit(textSurface, textRect)

    def quit(self):
        pygame.quit()
