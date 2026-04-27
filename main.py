import pygame
import random
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kernel import (
    GameScreen, MouseControl, GameState, GameStateManager,
    Player, Enemy, Bullet, Boss, Collision,
    EffectsManager, PowerUp, UI
)


class Game:
    def __init__(self):
        self.gameScreen = GameScreen()
        self.mouseControl = MouseControl(self.gameScreen)
        self.gameStateManager = GameStateManager()
        self.ui = UI(self.gameScreen)
        self.effects = EffectsManager()

        self.score = 0
        self.highScore = 0
        self.enemiesKilled = 0
        self.bossSpawnThreshold = 30
        self.boss = None

        self.player = None
        self.bullets = []
        self.enemyBullets = []
        self.enemies = []
        self.powerUps = []

        self.spawnTimer = 0
        self.spawnInterval = 60
        self.powerUpTimer = 0
        self.powerUpInterval = 300

        self.running = True
        self.clickCooldown = 0

    def resetGame(self):
        self.player = Player(self.gameScreen)
        self.bullets = []
        self.enemyBullets = []
        self.enemies = []
        self.powerUps = []
        self.effects.clearAll()
        self.score = 0
        self.enemiesKilled = 0
        self.boss = None
        self.spawnTimer = 0
        self.powerUpTimer = 0
        self.clickCooldown = 30

    def spawnEnemy(self):
        enemyType = random.choice([1, 1, 1, 2, 2, 3])
        x = random.randint(20, self.gameScreen.WIDTH - 60)
        enemy = Enemy(x, -50, enemyType)
        self.enemies.append(enemy)

    def spawnPowerUp(self):
        if random.random() < 0.3:
            x = random.randint(20, self.gameScreen.WIDTH - 60)
            powerUpType = random.randint(1, 5)
            powerUp = PowerUp(x, -40, powerUpType)
            self.powerUps.append(powerUp)

    def spawnBoss(self):
        if self.boss is None or not self.boss.isAlive:
            self.boss = Boss(self.gameScreen)
            self.gameStateManager.setState(GameState.BOSS)

    def update(self):
        self.mouseControl.update()

        if self.clickCooldown > 0:
            self.clickCooldown -= 1

        if self.gameStateManager.isMenu():
            self.updateMenu()
        elif self.gameStateManager.isPlaying() or self.gameStateManager.isBoss():
            self.updatePlaying()
        elif self.gameStateManager.isGameOver():
            self.updateGameOver()
        elif self.gameStateManager.isVictory():
            self.updateVictory()

    def updateMenu(self):
        if self.ui.isStartClicked(self.mouseControl) and self.clickCooldown == 0:
            self.resetGame()
            self.gameStateManager.setState(GameState.PLAYING)

    def updatePlaying(self):
        self.player.update(self.mouseControl)
        self.player.shoot(self.bullets)

        self.spawnTimer += 1
        if self.spawnTimer >= self.spawnInterval:
            self.spawnTimer = 0
            if self.enemiesKilled < self.bossSpawnThreshold:
                self.spawnEnemy()

        self.powerUpTimer += 1
        if self.powerUpTimer >= self.powerUpInterval:
            self.powerUpTimer = 0
            self.spawnPowerUp()

        for bullet in self.bullets[:]:
            bullet.update(self.gameScreen)
            if not bullet.isAlive:
                self.bullets.remove(bullet)

        for bullet in self.enemyBullets[:]:
            bullet.update(self.gameScreen)
            if not bullet.isAlive:
                self.enemyBullets.remove(bullet)

        for enemy in self.enemies[:]:
            enemy.update(self.gameScreen)
            if random.random() < 0.01:
                self.enemyBullets.append(Bullet(
                    enemy.x + enemy.width // 2,
                    enemy.y + enemy.height,
                    0, 5,
                    (255, 0, 100),
                    6, 15
                ))
            if not enemy.isAlive:
                self.enemies.remove(enemy)

        for powerUp in self.powerUps[:]:
            powerUp.update(self.gameScreen)
            if not powerUp.isAlive:
                self.powerUps.remove(powerUp)

        if self.enemiesKilled >= self.bossSpawnThreshold and (self.boss is None or not self.boss.isAlive):
            if len(self.enemies) == 0:
                self.spawnBoss()

        if self.gameStateManager.isBoss() and self.boss and self.boss.isAlive:
            self.boss.update()
            self.boss.shoot(self.enemyBullets)

        self.score = Collision.checkBulletsVsEnemies(self.bullets, self.enemies, self.score, self.effects)

        if self.boss and self.boss.isAlive:
            self.score = Collision.checkBulletsVsBoss(self.bullets, self.boss, self.score, self.effects)

        Collision.checkEnemyBulletsVsPlayer(self.enemyBullets, self.player, self.effects)
        Collision.checkEnemiesVsPlayer(self.enemies, self.player, self.effects)

        if self.boss and self.boss.isAlive and not self.boss.isEntering:
            Collision.checkBossVsPlayer(self.boss, self.player, self.effects)

        for powerUp in self.powerUps[:]:
            if Collision.checkCollision(powerUp.getRect(), self.player.getRect()):
                powerUp.apply(self.player, self.gameScreen, self.effects,
                            self.enemyBullets, self.enemies, self.boss)
                powerUp.isAlive = False
                self.powerUps.remove(powerUp)

        for enemy in self.enemies[:]:
            if not enemy.isAlive:
                self.enemiesKilled += 1
                self.enemies.remove(enemy)
                if random.random() < 0.15:
                    powerUpType = random.randint(1, 5)
                    powerUp = PowerUp(enemy.x, enemy.y, powerUpType)
                    self.powerUps.append(powerUp)

        if not self.player.isAlive:
            self.gameStateManager.setState(GameState.GAME_OVER)
            if self.score > self.highScore:
                self.highScore = self.score

        if self.boss and not self.boss.isAlive:
            self.gameStateManager.setState(GameState.VICTORY)
            if self.score > self.highScore:
                self.highScore = self.score

        self.effects.update()

    def updateGameOver(self):
        if self.ui.isRestartClicked(self.mouseControl) and self.clickCooldown == 0:
            self.resetGame()
            self.gameStateManager.setState(GameState.PLAYING)

    def updateVictory(self):
        if self.ui.isRestartClicked(self.mouseControl) and self.clickCooldown == 0:
            self.resetGame()
            self.gameStateManager.setState(GameState.PLAYING)

    def draw(self):
        self.gameScreen.fillBackground((0, 0, 30))

        if self.gameStateManager.isMenu():
            self.drawMenu()
        elif self.gameStateManager.isPlaying() or self.gameStateManager.isBoss():
            self.drawPlaying()
        elif self.gameStateManager.isGameOver():
            self.drawGameOver()
        elif self.gameStateManager.isVictory():
            self.drawVictory()

        self.gameScreen.updateDisplay()

    def drawMenu(self):
        self.ui.drawMenu(self.mouseControl)

    def drawPlaying(self):
        for powerUp in self.powerUps:
            powerUp.draw(self.gameScreen.getScreen())

        for enemy in self.enemies:
            enemy.draw(self.gameScreen.getScreen())

        if self.boss and self.boss.isAlive:
            self.boss.draw(self.gameScreen.getScreen())

        self.player.draw(self.gameScreen.getScreen())

        for bullet in self.bullets:
            bullet.draw(self.gameScreen.getScreen())

        for bullet in self.enemyBullets:
            bullet.draw(self.gameScreen.getScreen())

        self.effects.draw(self.gameScreen.getScreen())

        self.ui.drawGameUI(self.score, self.player, self.boss)

    def drawGameOver(self):
        self.ui.drawGameOver(self.score, self.mouseControl)

    def drawVictory(self):
        self.ui.drawVictory(self.score, self.mouseControl)

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def run(self):
        while self.running:
            self.handleEvents()
            self.update()
            self.draw()
            self.gameScreen.tick()

        self.gameScreen.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
