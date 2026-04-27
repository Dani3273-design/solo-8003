import pygame
import random


class Player:
    def __init__(self, gameScreen):
        self.gameScreen = gameScreen
        self.width = 40
        self.height = 50
        self.x = gameScreen.WIDTH // 2 - self.width // 2
        self.y = gameScreen.HEIGHT - self.height - 50
        self.speed = 5
        self.health = 100
        self.maxHealth = 100
        self.fireRate = 150
        self.lastFireTime = 0
        self.isAlive = True

    def update(self, mouseControl):
        mouseX, mouseY = mouseControl.getPos()
        self.x = mouseX - self.width // 2
        self.y = mouseY - self.height // 2

        self.x = max(0, min(self.x, self.gameScreen.WIDTH - self.width))
        self.y = max(0, min(self.y, self.gameScreen.HEIGHT - self.height))

    def draw(self, screen):
        pygame.draw.polygon(screen, (0, 200, 255), [
            (self.x + self.width // 2, self.y),
            (self.x, self.y + self.height),
            (self.x + self.width // 4, self.y + self.height * 0.7),
            (self.x + self.width // 2, self.y + self.height * 0.9),
            (self.x + self.width * 3 // 4, self.y + self.height * 0.7),
            (self.x + self.width, self.y + self.height)
        ])
        pygame.draw.polygon(screen, (255, 100, 0), [
            (self.x + self.width // 3, self.y + self.height),
            (self.x + self.width // 2, self.y + self.height + 10 + random.randint(0, 10)),
            (self.x + self.width * 2 // 3, self.y + self.height)
        ])

    def getRect(self):
        return pygame.Rect(self.x + 10, self.y + 10, self.width - 20, self.height - 20)

    def shoot(self, bullets):
        currentTime = pygame.time.get_ticks()
        if currentTime - self.lastFireTime > self.fireRate:
            bullets.append(Bullet(
                self.x + self.width // 2 - 2,
                self.y,
                0, -10,
                (0, 255, 255),
                4, 15
            ))
            bullets.append(Bullet(
                self.x + self.width // 2 - 15,
                self.y + 20,
                -1, -10,
                (0, 255, 255),
                3, 10
            ))
            bullets.append(Bullet(
                self.x + self.width // 2 + 12,
                self.y + 20,
                1, -10,
                (0, 255, 255),
                3, 10
            ))
            self.lastFireTime = currentTime

    def takeDamage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.isAlive = False


class Enemy:
    def __init__(self, x, y, enemyType):
        self.x = x
        self.y = y
        self.enemyType = enemyType
        self.isAlive = True

        if enemyType == 1:
            self.width = 30
            self.height = 30
            self.speedY = 3
            self.speedX = 0
            self.health = 20
            self.maxHealth = 20
            self.score = 100
            self.color = (255, 100, 100)
        elif enemyType == 2:
            self.width = 40
            self.height = 40
            self.speedY = 2
            self.speedX = random.choice([-1, 1]) * 2
            self.health = 40
            self.maxHealth = 40
            self.score = 200
            self.color = (255, 200, 100)
        else:
            self.width = 35
            self.height = 35
            self.speedY = 4
            self.speedX = 0
            self.health = 10
            self.maxHealth = 10
            self.score = 50
            self.color = (200, 100, 255)

    def update(self, gameScreen):
        self.y += self.speedY
        self.x += self.speedX

        if self.x <= 0 or self.x >= gameScreen.WIDTH - self.width:
            self.speedX *= -1

        if self.y > gameScreen.HEIGHT:
            self.isAlive = False

    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, [
            (self.x + self.width // 2, self.y + self.height),
            (self.x, self.y),
            (self.x + self.width // 2, self.y + self.height * 0.3),
            (self.x + self.width, self.y)
        ])

    def getRect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def takeDamage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.isAlive = False
            return True
        return False


class Boss:
    def __init__(self, gameScreen):
        self.gameScreen = gameScreen
        self.width = 120
        self.height = 100
        self.x = gameScreen.WIDTH // 2 - self.width // 2
        self.y = -self.height
        self.targetY = 50
        self.speedY = 2
        self.speedX = 3
        self.directionX = 1
        self.health = 1000
        self.maxHealth = 1000
        self.isAlive = True
        self.isEntering = True
        self.lastFireTime = 0
        self.fireRate = 800
        self.pattern = 0
        self.patternTimer = 0

    def update(self):
        if self.isEntering:
            self.y += self.speedY
            if self.y >= self.targetY:
                self.y = self.targetY
                self.isEntering = False
            return

        self.x += self.speedX * self.directionX
        if self.x <= 0:
            self.x = 0
            self.directionX = 1
        elif self.x >= self.gameScreen.WIDTH - self.width:
            self.x = self.gameScreen.WIDTH - self.width
            self.directionX = -1

        self.patternTimer += 1
        if self.patternTimer > 120:
            self.patternTimer = 0
            self.pattern = (self.pattern + 1) % 3

    def draw(self, screen):
        pygame.draw.polygon(screen, (150, 0, 200), [
            (self.x + self.width // 2, self.y),
            (self.x, self.y + self.height),
            (self.x + self.width // 4, self.y + self.height * 0.6),
            (self.x + self.width * 3 // 4, self.y + self.height * 0.6),
            (self.x + self.width, self.y + self.height)
        ])

        pygame.draw.polygon(screen, (255, 0, 100), [
            (self.x + self.width // 2, self.y + self.height),
            (self.x + self.width // 3, self.y + self.height * 0.7),
            (self.x + self.width * 2 // 3, self.y + self.height * 0.7)
        ])

        pygame.draw.circle(screen, (255, 50, 50),
                          (self.x + self.width // 2, self.y + self.height // 3), 20)
        pygame.draw.circle(screen, (255, 100, 100),
                          (self.x + self.width // 2, self.y + self.height // 3), 10)

    def getRect(self):
        return pygame.Rect(self.x + 20, self.y + 20, self.width - 40, self.height - 40)

    def shoot(self, enemyBullets):
        if self.isEntering:
            return

        currentTime = pygame.time.get_ticks()
        if currentTime - self.lastFireTime > self.fireRate:
            self.lastFireTime = currentTime

            if self.pattern == 0:
                for i in range(-2, 3):
                    enemyBullets.append(Bullet(
                        self.x + self.width // 2 - 3,
                        self.y + self.height,
                        i * 2, 6,
                        (255, 0, 255),
                        8, 20
                    ))
            elif self.pattern == 1:
                enemyBullets.append(Bullet(
                    self.x + self.width // 4,
                    self.y + self.height,
                    -1, 7,
                    (255, 100, 0),
                    10, 25
                ))
                enemyBullets.append(Bullet(
                    self.x + self.width * 3 // 4,
                    self.y + self.height,
                    1, 7,
                    (255, 100, 0),
                    10, 25
                ))
            else:
                enemyBullets.append(Bullet(
                    self.x + self.width // 2,
                    self.y + self.height,
                    0, 8,
                    (0, 255, 0),
                    15, 30
                ))

    def takeDamage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.isAlive = False
            return True
        return False


class Bullet:
    def __init__(self, x, y, speedX, speedY, color, size, damage):
        self.x = x
        self.y = y
        self.speedX = speedX
        self.speedY = speedY
        self.color = color
        self.size = size
        self.damage = damage
        self.isAlive = True

    def update(self, gameScreen):
        self.x += self.speedX
        self.y += self.speedY

        if (self.y < -20 or self.y > gameScreen.HEIGHT + 20 or
                self.x < -20 or self.x > gameScreen.WIDTH + 20):
            self.isAlive = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color,
                        (self.x, self.y, self.size, self.size * 2))
        pygame.draw.rect(screen, (255, 255, 255),
                        (self.x + self.size // 4, self.y,
                         self.size // 2, self.size * 2))

    def getRect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size * 2)
