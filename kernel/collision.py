import pygame


class Collision:
    @staticmethod
    def checkCollision(rect1, rect2):
        return rect1.colliderect(rect2)

    @staticmethod
    def checkBulletsVsEnemies(bullets, enemies, score, effects):
        for bullet in bullets[:]:
            if not bullet.isAlive:
                continue

            for enemy in enemies[:]:
                if not enemy.isAlive:
                    continue

                if Collision.checkCollision(bullet.getRect(), enemy.getRect()):
                    bullet.isAlive = False
                    if enemy.takeDamage(bullet.damage):
                        score += enemy.score
                        effects.addExplosion(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2)
                    break

        return score

    @staticmethod
    def checkBulletsVsBoss(bullets, boss, score, effects):
        if not boss or not boss.isAlive:
            return score

        for bullet in bullets[:]:
            if not bullet.isAlive:
                continue

            if Collision.checkCollision(bullet.getRect(), boss.getRect()):
                bullet.isAlive = False
                if boss.takeDamage(bullet.damage):
                    score += 5000
                    for i in range(5):
                        effects.addExplosion(
                            boss.x + boss.width // 4 + i * (boss.width // 5),
                            boss.y + boss.height // 2
                        )

        return score

    @staticmethod
    def checkEnemyBulletsVsPlayer(enemyBullets, player, effects):
        if not player.isAlive:
            return

        for bullet in enemyBullets[:]:
            if not bullet.isAlive:
                continue

            if Collision.checkCollision(bullet.getRect(), player.getRect()):
                bullet.isAlive = False
                player.takeDamage(bullet.damage)
                effects.addSpark(player.x + player.width // 2, player.y + player.height // 2)

    @staticmethod
    def checkEnemiesVsPlayer(enemies, player, effects):
        if not player.isAlive:
            return

        for enemy in enemies[:]:
            if not enemy.isAlive:
                continue

            if Collision.checkCollision(enemy.getRect(), player.getRect()):
                enemy.isAlive = False
                player.takeDamage(30)
                effects.addExplosion(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2)

    @staticmethod
    def checkBossVsPlayer(boss, player, effects):
        if not boss or not boss.isAlive or not player.isAlive:
            return

        if Collision.checkCollision(boss.getRect(), player.getRect()):
            player.takeDamage(50)
            effects.addSpark(player.x + player.width // 2, player.y + player.height // 2)
