import pygame
import random
import math


class Player:
    def __init__(self, gameScreen):
        self.gameScreen = gameScreen
        self.width = 50
        self.height = 60
        self.x = gameScreen.WIDTH // 2 - self.width // 2
        self.y = gameScreen.HEIGHT - self.height - 50
        self.speed = 5
        self.health = 100
        self.maxHealth = 100
        self.fireRate = 150
        self.lastFireTime = 0
        self.isAlive = True
        self.animFrame = 0

    def update(self, mouseControl):
        mouseX, mouseY = mouseControl.getPos()
        self.x = mouseX - self.width // 2
        self.y = mouseY - self.height // 2

        self.x = max(0, min(self.x, self.gameScreen.WIDTH - self.width))
        self.y = max(0, min(self.y, self.gameScreen.HEIGHT - self.height))
        self.animFrame = (self.animFrame + 1) % 60

    def draw(self, screen):
        cx = self.x + self.width // 2
        cy = self.y + self.height // 2

        wingFlare = 150 + int(math.sin(self.animFrame * 0.3) * 30)
        wingColor = (0, wingFlare, 255)

        pygame.draw.polygon(screen, wingColor, [
            (cx - 5, self.y + 15),
            (self.x, self.y + self.height - 10),
            (cx - 8, self.y + self.height - 25)
        ])
        pygame.draw.polygon(screen, wingColor, [
            (cx + 5, self.y + 15),
            (self.x + self.width, self.y + self.height - 10),
            (cx + 8, self.y + self.height - 25)
        ])

        pygame.draw.polygon(screen, (0, 180, 220), [
            (cx, self.y),
            (cx - 12, self.y + 25),
            (cx - 8, self.y + self.height - 15),
            (cx + 8, self.y + self.height - 15),
            (cx + 12, self.y + 25)
        ])

        pygame.draw.polygon(screen, (0, 100, 150), [
            (cx, self.y + 5),
            (cx - 8, self.y + 20),
            (cx - 5, self.y + self.height - 20),
            (cx + 5, self.y + self.height - 20),
            (cx + 8, self.y + 20)
        ])

        cockpitGlow = 200 + int(math.sin(self.animFrame * 0.2) * 55)
        pygame.draw.ellipse(screen, (cockpitGlow, cockpitGlow, 255),
                           (cx - 6, self.y + 12, 12, 18))
        pygame.draw.ellipse(screen, (255, 255, 255),
                           (cx - 4, self.y + 14, 8, 12), 1)

        engineGlow = 150 + int(math.sin(self.animFrame * 0.8) * 100)
        flameLength = 15 + int(math.sin(self.animFrame * 0.9) * 8)

        pygame.draw.polygon(screen, (255, engineGlow, 0), [
            (cx - 10, self.y + self.height - 10),
            (cx - 5, self.y + self.height + flameLength),
            (cx - 2, self.y + self.height - 5)
        ])
        pygame.draw.polygon(screen, (255, engineGlow, 0), [
            (cx + 10, self.y + self.height - 10),
            (cx + 5, self.y + self.height + flameLength),
            (cx + 2, self.y + self.height - 5)
        ])

        pygame.draw.polygon(screen, (255, 255, 200), [
            (cx - 6, self.y + self.height - 8),
            (cx - 3, self.y + self.height + flameLength - 5),
            (cx, self.y + self.height - 5)
        ])
        pygame.draw.polygon(screen, (255, 255, 200), [
            (cx + 6, self.y + self.height - 8),
            (cx + 3, self.y + self.height + flameLength - 5),
            (cx, self.y + self.height - 5)
        ])

        pygame.draw.rect(screen, (200, 200, 200),
                        (cx - 18, self.y + self.height - 18, 6, 8))
        pygame.draw.rect(screen, (200, 200, 200),
                        (cx + 12, self.y + self.height - 18, 6, 8))

    def getRect(self):
        return pygame.Rect(self.x + 10, self.y + 10, self.width - 20, self.height - 20)

    def shoot(self, bullets):
        currentTime = pygame.time.get_ticks()
        if currentTime - self.lastFireTime > self.fireRate:
            bullets.append(Bullet(
                self.x + self.width // 2 - 2,
                self.y + 5,
                0, -12,
                (0, 255, 255),
                4, 15
            ))
            bullets.append(Bullet(
                self.x + self.width // 2 - 18,
                self.y + 25,
                -2, -11,
                (0, 200, 255),
                3, 10
            ))
            bullets.append(Bullet(
                self.x + self.width // 2 + 15,
                self.y + 25,
                2, -11,
                (0, 200, 255),
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
        self.animFrame = random.randint(0, 60)

        if enemyType == 1:
            self.width = 35
            self.height = 35
            self.speedY = 3
            self.speedX = 0
            self.health = 20
            self.maxHealth = 20
            self.score = 100
            self.color = (255, 80, 80)
        elif enemyType == 2:
            self.width = 45
            self.height = 45
            self.speedY = 2
            self.speedX = random.choice([-1, 1]) * 2
            self.health = 40
            self.maxHealth = 40
            self.score = 200
            self.color = (255, 180, 50)
        else:
            self.width = 30
            self.height = 30
            self.speedY = 4
            self.speedX = 0
            self.health = 10
            self.maxHealth = 10
            self.score = 50
            self.color = (180, 80, 255)

    def update(self, gameScreen):
        self.y += self.speedY
        self.x += self.speedX
        self.animFrame = (self.animFrame + 1) % 60

        if self.x <= 0 or self.x >= gameScreen.WIDTH - self.width:
            self.speedX *= -1

        if self.y > gameScreen.HEIGHT:
            self.isAlive = False

    def draw(self, screen):
        cx = self.x + self.width // 2
        cy = self.y + self.height // 2
        glow = 100 + int(math.sin(self.animFrame * 0.3) * 50)

        if self.enemyType == 1:
            pygame.draw.polygon(screen, self.color, [
                (cx, self.y + self.height),
                (self.x, self.y),
                (cx - 5, self.y + self.height * 0.4),
                (cx, self.y + self.height * 0.2),
                (cx + 5, self.y + self.height * 0.4),
                (self.x + self.width, self.y)
            ])
            pygame.draw.polygon(screen, (self.color[0] - 50, self.color[1] - 50, self.color[2] - 50), [
                (cx, self.y + self.height - 5),
                (cx - 8, self.y + 8),
                (cx, self.y + 12),
                (cx + 8, self.y + 8)
            ])
            pygame.draw.circle(screen, (255, glow, glow), (cx, self.y + 15), 5)

        elif self.enemyType == 2:
            pygame.draw.polygon(screen, self.color, [
                (cx, self.y + self.height),
                (self.x, self.y + 10),
                (cx - 12, self.y + self.height * 0.6),
                (cx - 6, self.y + 5),
                (cx, self.y),
                (cx + 6, self.y + 5),
                (cx + 12, self.y + self.height * 0.6),
                (self.x + self.width, self.y + 10)
            ])
            pygame.draw.polygon(screen, (self.color[0] - 30, self.color[1] - 30, self.color[2] - 30), [
                (cx, self.y + self.height - 10),
                (cx - 10, self.y + 15),
                (cx, self.y + 20),
                (cx + 10, self.y + 15)
            ])
            pygame.draw.circle(screen, (glow, glow, 50), (cx, self.y + 20), 6)
            pygame.draw.rect(screen, (150, 150, 150),
                            (self.x + 3, self.y + self.height - 15, 8, 10))
            pygame.draw.rect(screen, (150, 150, 150),
                            (self.x + self.width - 11, self.y + self.height - 15, 8, 10))

        else:
            pygame.draw.polygon(screen, self.color, [
                (cx, self.y + self.height),
                (self.x, self.y + 5),
                (cx, self.y + self.height * 0.3),
                (self.x + self.width, self.y + 5)
            ])
            pygame.draw.polygon(screen, (self.color[0] - 40, self.color[1] - 40, self.color[2] - 40), [
                (cx, self.y + self.height - 5),
                (cx - 6, self.y + 10),
                (cx, self.y + 15),
                (cx + 6, self.y + 10)
            ])
            pygame.draw.circle(screen, (glow, 50, glow), (cx, self.y + 12), 4)

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
        self.width = 130
        self.height = 110
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
        self.animFrame = 0

    def update(self):
        self.animFrame = (self.animFrame + 1) % 120

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
        cx = self.x + self.width // 2
        cy = self.y + self.height // 2
        glow = 120 + int(math.sin(self.animFrame * 0.15) * 80)
        pulseGlow = 200 + int(math.sin(self.animFrame * 0.2) * 55)

        pygame.draw.polygon(screen, (150, 0, 180), [
            (cx, self.y),
            (self.x, self.y + self.height * 0.4),
            (self.x + 10, self.y + self.height),
            (cx - 25, self.y + self.height * 0.7),
            (cx, self.y + self.height * 0.5),
            (cx + 25, self.y + self.height * 0.7),
            (self.x + self.width - 10, self.y + self.height),
            (self.x + self.width, self.y + self.height * 0.4)
        ])

        pygame.draw.polygon(screen, (100, 0, 130), [
            (cx, self.y + 10),
            (self.x + 15, self.y + self.height * 0.4),
            (self.x + 20, self.y + self.height - 15),
            (cx - 20, self.y + self.height * 0.7),
            (cx, self.y + self.height * 0.55),
            (cx + 20, self.y + self.height * 0.7),
            (self.x + self.width - 20, self.y + self.height - 15),
            (self.x + self.width - 15, self.y + self.height * 0.4)
        ])

        pygame.draw.polygon(screen, (180, 20, 80), [
            (cx - 20, self.y + self.height),
            (cx - 35, self.y + self.height - 20),
            (cx - 10, self.y + self.height - 35),
            (cx + 10, self.y + self.height - 35),
            (cx + 35, self.y + self.height - 20),
            (cx + 20, self.y + self.height)
        ])

        coreGlow = min(255, glow + 100)
        pygame.draw.circle(screen, (coreGlow, 50, 80),
                          (cx, self.y + self.height // 3), 25)
        pygame.draw.circle(screen, (pulseGlow, 100, 120),
                          (cx, self.y + self.height // 3), 18)
        pygame.draw.circle(screen, (255, 200, 200),
                          (cx, self.y + self.height // 3), 10)

        pygame.draw.rect(screen, (glow, 0, glow),
                        (self.x + 8, self.y + self.height - 30, 18, 25), border_radius=3)
        pygame.draw.rect(screen, (glow, 0, glow),
                        (self.x + self.width - 26, self.y + self.height - 30, 18, 25), border_radius=3)

        pygame.draw.rect(screen, (255, 150, 0),
                        (self.x + 12, self.y + self.height - 25, 10, 18), border_radius=2)
        pygame.draw.rect(screen, (255, 150, 0),
                        (self.x + self.width - 22, self.y + self.height - 25, 10, 18), border_radius=2)

        pygame.draw.line(screen, (180, 180, 200),
                        (cx - 35, self.y + 25), (cx - 45, self.y + 10), 3)
        pygame.draw.line(screen, (180, 180, 200),
                        (cx + 35, self.y + 25), (cx + 45, self.y + 10), 3)

        antennaGlow = 150 + int(math.sin(self.animFrame * 0.4) * 100)
        pygame.draw.circle(screen, (antennaGlow, antennaGlow, 255),
                          (cx - 45, self.y + 10), 4)
        pygame.draw.circle(screen, (antennaGlow, antennaGlow, 255),
                          (cx + 45, self.y + 10), 4)

    def getRect(self):
        return pygame.Rect(self.x + 20, self.y + 20, self.width - 40, self.height - 40)

    def shoot(self, enemyBullets):
        if self.isEntering:
            return

        currentTime = pygame.time.get_ticks()
        if currentTime - self.lastFireTime > self.fireRate:
            self.lastFireTime = currentTime

            if self.pattern == 0:
                for i in range(-3, 4):
                    enemyBullets.append(Bullet(
                        self.x + self.width // 2 - 4,
                        self.y + self.height,
                        i * 1.8, 5,
                        (255, 0, 255),
                        8, 20
                    ))
            elif self.pattern == 1:
                enemyBullets.append(Bullet(
                    self.x + self.width // 5,
                    self.y + self.height,
                    -1.5, 6,
                    (255, 100, 0),
                    10, 25
                ))
                enemyBullets.append(Bullet(
                    self.x + self.width * 4 // 5,
                    self.y + self.height,
                    1.5, 6,
                    (255, 100, 0),
                    10, 25
                ))
            else:
                enemyBullets.append(Bullet(
                    self.x + self.width // 2,
                    self.y + self.height,
                    0, 7,
                    (0, 255, 50),
                    14, 30
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
        self.animFrame = 0

    def update(self, gameScreen):
        self.x += self.speedX
        self.y += self.speedY
        self.animFrame = (self.animFrame + 1) % 30

        if (self.y < -20 or self.y > gameScreen.HEIGHT + 20 or
                self.x < -20 or self.x > gameScreen.WIDTH + 20):
            self.isAlive = False

    def draw(self, screen):
        glow = 0.5 + math.sin(self.animFrame * 0.5) * 0.3

        if self.speedY < 0:
            pygame.draw.rect(screen, (
                int(self.color[0] * glow),
                int(self.color[1] * glow),
                int(self.color[2] * glow)
            ), (self.x - 1, self.y - 1, self.size + 2, self.size * 2 + 2))
            pygame.draw.rect(screen, self.color,
                            (self.x, self.y, self.size, self.size * 2))
            pygame.draw.rect(screen, (255, 255, 255),
                            (self.x + self.size // 4, self.y + 1,
                             self.size // 2, self.size * 2 - 2))
        else:
            pygame.draw.ellipse(screen, (
                int(self.color[0] * glow),
                int(self.color[1] * glow),
                int(self.color[2] * glow)
            ), (self.x - 2, self.y - 2, self.size + 4, self.size * 2 + 4))
            pygame.draw.ellipse(screen, self.color,
                               (self.x, self.y, self.size, self.size * 2))
            pygame.draw.ellipse(screen, (255, 255, 255),
                               (self.x + self.size // 4, self.y + self.size // 2,
                                self.size // 2, self.size))

    def getRect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size * 2)
