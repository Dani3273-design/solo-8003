import pygame


class Button:
    def __init__(self, x, y, width, height, text, color=(100, 100, 255), hoverColor=(150, 150, 255)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.hoverColor = hoverColor
        self.rect = pygame.Rect(x, y, width, height)
        self.isHovered = False
        self.font = pygame.font.SysFont("arial", 28)

    def update(self, mouseControl):
        mousePos = mouseControl.getPos()
        self.isHovered = mouseControl.isPointInRect(mousePos, self.rect)

    def draw(self, screen):
        color = self.hoverColor if self.isHovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 3)

        textSurface = self.font.render(self.text, True, (255, 255, 255))
        textRect = textSurface.get_rect()
        textRect.centerx = self.rect.centerx
        textRect.centery = self.rect.centery
        screen.blit(textSurface, textRect)

    def isClicked(self, mouseControl):
        return self.isHovered and mouseControl.isMouseDown()


class UI:
    def __init__(self, gameScreen):
        self.gameScreen = gameScreen
        self.screen = gameScreen.getScreen()
        self.font = pygame.font.SysFont("arial", 24)
        self.bigFont = pygame.font.SysFont("arial", 48)

        centerX = gameScreen.WIDTH // 2
        self.startButton = Button(
            centerX - 100, 400, 200, 60, "开始游戏",
            (0, 150, 0), (0, 200, 0)
        )
        self.restartButton = Button(
            centerX - 100, 450, 200, 60, "重新开始",
            (150, 100, 0), (200, 150, 0)
        )

    def drawMenu(self, mouseControl):
        titleText = self.bigFont.render("雷 电", True, (255, 255, 0))
        titleRect = titleText.get_rect()
        titleRect.centerx = self.gameScreen.WIDTH // 2
        titleRect.top = 150
        self.screen.blit(titleText, titleRect)

        subTitle = self.font.render("纵卷轴射击游戏", True, (200, 200, 200))
        subTitleRect = subTitle.get_rect()
        subTitleRect.centerx = self.gameScreen.WIDTH // 2
        subTitleRect.top = 230
        self.screen.blit(subTitle, subTitleRect)

        instruction = self.font.render("使用鼠标移动控制飞机", True, (150, 150, 255))
        instructionRect = instruction.get_rect()
        instructionRect.centerx = self.gameScreen.WIDTH // 2
        instructionRect.top = 320
        self.screen.blit(instruction, instructionRect)

        self.startButton.update(mouseControl)
        self.startButton.draw(self.screen)

    def drawGameUI(self, score, player, boss=None):
        scoreText = self.font.render(f"分数: {score}", True, (255, 255, 255))
        self.screen.blit(scoreText, (10, 10))

        healthText = self.font.render("生命:", True, (255, 255, 255))
        self.screen.blit(healthText, (10, 40))

        healthWidth = 100
        healthHeight = 20
        healthX = 70
        healthY = 42

        pygame.draw.rect(self.screen, (100, 100, 100),
                        (healthX, healthY, healthWidth, healthHeight))

        healthPercent = player.health / player.maxHealth
        healthColor = (0, 255, 0) if healthPercent > 0.5 else (255, 255, 0) if healthPercent > 0.25 else (255, 0, 0)
        pygame.draw.rect(self.screen, healthColor,
                        (healthX, healthY, healthWidth * healthPercent, healthHeight))

        pygame.draw.rect(self.screen, (255, 255, 255),
                        (healthX, healthY, healthWidth, healthHeight), 2)

        if boss and boss.isAlive and not boss.isEntering:
            bossHealthWidth = self.gameScreen.WIDTH - 40
            bossHealthHeight = 25
            bossHealthX = 20
            bossHealthY = self.gameScreen.HEIGHT - 50

            bossText = self.font.render("BOSS", True, (255, 0, 255))
            bossTextRect = bossText.get_rect()
            bossTextRect.centerx = self.gameScreen.WIDTH // 2
            bossTextRect.top = bossHealthY - 25
            self.screen.blit(bossText, bossTextRect)

            pygame.draw.rect(self.screen, (50, 50, 50),
                            (bossHealthX, bossHealthY, bossHealthWidth, bossHealthHeight))

            bossHealthPercent = boss.health / boss.maxHealth
            pygame.draw.rect(self.screen, (255, 0, 100),
                            (bossHealthX, bossHealthY,
                             bossHealthWidth * bossHealthPercent, bossHealthHeight))

            pygame.draw.rect(self.screen, (255, 100, 200),
                            (bossHealthX, bossHealthY, bossHealthWidth, bossHealthHeight), 2)

    def drawGameOver(self, score, mouseControl):
        overlay = pygame.Surface((self.gameScreen.WIDTH, self.gameScreen.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        gameOverText = self.bigFont.render("游戏结束", True, (255, 50, 50))
        gameOverRect = gameOverText.get_rect()
        gameOverRect.centerx = self.gameScreen.WIDTH // 2
        gameOverRect.top = 200
        self.screen.blit(gameOverText, gameOverRect)

        finalScore = self.font.render(f"最终分数: {score}", True, (255, 255, 255))
        finalScoreRect = finalScore.get_rect()
        finalScoreRect.centerx = self.gameScreen.WIDTH // 2
        finalScoreRect.top = 300
        self.screen.blit(finalScore, finalScoreRect)

        self.restartButton.update(mouseControl)
        self.restartButton.draw(self.screen)

    def drawVictory(self, score, mouseControl):
        overlay = pygame.Surface((self.gameScreen.WIDTH, self.gameScreen.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        victoryText = self.bigFont.render("胜 利!", True, (255, 255, 0))
        victoryRect = victoryText.get_rect()
        victoryRect.centerx = self.gameScreen.WIDTH // 2
        victoryRect.top = 200
        self.screen.blit(victoryText, victoryRect)

        finalScore = self.font.render(f"最终分数: {score}", True, (255, 255, 255))
        finalScoreRect = finalScore.get_rect()
        finalScoreRect.centerx = self.gameScreen.WIDTH // 2
        finalScoreRect.top = 300
        self.screen.blit(finalScore, finalScoreRect)

        congrats = self.font.render("恭喜你击败了BOSS!", True, (100, 255, 100))
        congratsRect = congrats.get_rect()
        congratsRect.centerx = self.gameScreen.WIDTH // 2
        congratsRect.top = 380
        self.screen.blit(congrats, congratsRect)

        self.restartButton.update(mouseControl)
        self.restartButton.draw(self.screen)

    def isStartClicked(self, mouseControl):
        return self.startButton.isClicked(mouseControl)

    def isRestartClicked(self, mouseControl):
        return self.restartButton.isClicked(mouseControl)
