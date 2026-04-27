import pygame
import random


class Effect:
    def __init__(self, x, y, effectType, duration=30):
        self.x = x
        self.y = y
        self.effectType = effectType
        self.duration = duration
        self.maxDuration = duration
        self.isAlive = True

    def update(self):
        self.duration -= 1
        if self.duration <= 0:
            self.isAlive = False

    def draw(self, screen):
        progress = self.duration / self.maxDuration

        if self.effectType == "explosion":
            size = int(30 * (1 - progress) + 10)
            alpha = int(255 * progress)
            pygame.draw.circle(screen, (255, 100 + int(155 * progress), 0),
                              (self.x, self.y), size)
            pygame.draw.circle(screen, (255, 255, 0),
                              (self.x, self.y), size // 2)

        elif self.effectType == "spark":
            size = int(20 * (1 - progress) + 5)
            pygame.draw.circle(screen, (255, 255, 255),
                              (self.x, self.y), size)

        elif self.effectType == "powerUp":
            size = int(25 * (1 - progress) + 10)
            color = (0, 255, 100) if progress > 0.5 else (100, 255, 255)
            pygame.draw.circle(screen, color, (self.x, self.y), size)

        elif self.effectType == "screenClear":
            size = int(400 * (1 - progress))
            for i in range(8):
                angle = i * 45 + (1 - progress) * 30
                import math
                endX = self.x + int(math.cos(math.radians(angle)) * size)
                endY = self.y + int(math.sin(math.radians(angle)) * size)
                pygame.draw.line(screen, (255, 200, 0),
                                (self.x, self.y), (endX, endY),
                                max(1, int(10 * progress)))

        elif self.effectType == "shield":
            size = int(60 * progress + 40)
            pygame.draw.circle(screen, (0, 200, 255),
                              (self.x, self.y), size, 5)


class EffectsManager:
    def __init__(self):
        self.effects = []

    def addExplosion(self, x, y):
        self.effects.append(Effect(x, y, "explosion", 30))

    def addSpark(self, x, y):
        self.effects.append(Effect(x, y, "spark", 15))

    def addPowerUp(self, x, y):
        self.effects.append(Effect(x, y, "powerUp", 40))

    def addScreenClear(self, x, y):
        self.effects.append(Effect(x, y, "screenClear", 60))

    def addShield(self, x, y):
        self.effects.append(Effect(x, y, "shield", 50))

    def update(self):
        for effect in self.effects[:]:
            effect.update()
            if not effect.isAlive:
                self.effects.remove(effect)

    def draw(self, screen):
        for effect in self.effects:
            effect.draw(screen)

    def clearAll(self):
        self.effects = []


class PowerUp:
    def __init__(self, x, y, powerUpType):
        self.x = x
        self.y = y
        self.powerUpType = powerUpType
        self.width = 30
        self.height = 30
        self.speedY = 2
        self.isAlive = True
        self.angle = 0

        self.powerUpTypes = {
            1: {"color": (255, 0, 0), "name": "health", "description": "恢复生命"},
            2: {"color": (0, 255, 0), "name": "fireRate", "description": "提升射速"},
            3: {"color": (0, 0, 255), "name": "shield", "description": "护盾"},
            4: {"color": (255, 255, 0), "name": "power", "description": "强化攻击"},
            5: {"color": (255, 0, 255), "name": "bomb", "description": "清屏炸弹"}
        }

    def update(self, gameScreen):
        self.y += self.speedY
        self.angle += 5

        if self.y > gameScreen.HEIGHT:
            self.isAlive = False

    def draw(self, screen):
        info = self.powerUpTypes.get(self.powerUpType, self.powerUpTypes[1])

        pygame.draw.circle(screen, info["color"],
                          (self.x + self.width // 2, self.y + self.height // 2),
                          self.width // 2)
        pygame.draw.circle(screen, (255, 255, 255),
                          (self.x + self.width // 2, self.y + self.height // 2),
                          self.width // 2, 2)

        if self.powerUpType == 1:
            pygame.draw.line(screen, (255, 255, 255),
                           (self.x + self.width // 2, self.y + 8),
                           (self.x + self.width // 2, self.y + self.height - 8), 3)
            pygame.draw.line(screen, (255, 255, 255),
                           (self.x + 8, self.y + self.height // 2),
                           (self.x + self.width - 8, self.y + self.height // 2), 3)
        elif self.powerUpType == 2:
            pygame.draw.rect(screen, (255, 255, 255),
                           (self.x + 10, self.y + 8, 4, 14))
            pygame.draw.rect(screen, (255, 255, 255),
                           (self.x + 16, self.y + 8, 4, 14))
        elif self.powerUpType == 3:
            pygame.draw.arc(screen, (255, 255, 255),
                           (self.x + 4, self.y + 4, self.width - 8, self.height - 8),
                           3.14, 0, 3)
        elif self.powerUpType == 4:
            pygame.draw.polygon(screen, (255, 255, 255), [
                (self.x + self.width // 2, self.y + 5),
                (self.x + 8, self.y + self.height // 2),
                (self.x + self.width // 2, self.y + self.height - 5),
                (self.x + self.width - 8, self.y + self.height // 2)
            ])
        elif self.powerUpType == 5:
            pygame.draw.circle(screen, (255, 255, 255),
                              (self.x + self.width // 2, self.y + self.height // 2), 8)
            pygame.draw.line(screen, (255, 255, 255),
                           (self.x + self.width // 2, self.y + 5),
                           (self.x + self.width // 2, self.y + 2), 2)

    def getRect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def apply(self, player, gameScreen, effects, enemyBullets, enemies, boss):
        info = self.powerUpTypes.get(self.powerUpType, self.powerUpTypes[1])

        if self.powerUpType == 1:
            player.health = min(player.health + 30, player.maxHealth)
            effects.addPowerUp(self.x, self.y)
        elif self.powerUpType == 2:
            player.fireRate = max(player.fireRate - 30, 50)
            effects.addPowerUp(self.x, self.y)
        elif self.powerUpType == 3:
            player.health = min(player.health + 20, player.maxHealth)
            effects.addShield(self.x, self.y)
        elif self.powerUpType == 4:
            player.fireRate = max(player.fireRate - 50, 40)
            player.health = min(player.health + 10, player.maxHealth)
            effects.addPowerUp(self.x, self.y)
        elif self.powerUpType == 5:
            effects.addScreenClear(gameScreen.WIDTH // 2, gameScreen.HEIGHT // 2)
            for bullet in enemyBullets:
                bullet.isAlive = False
            for enemy in enemies:
                enemy.isAlive = False
                effects.addExplosion(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2)
            if boss and boss.isAlive:
                boss.takeDamage(100)
