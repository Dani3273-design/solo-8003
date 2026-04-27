from enum import Enum


class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "gameOver"
    BOSS = "boss"
    VICTORY = "victory"


class GameStateManager:
    def __init__(self):
        self.currentState = GameState.MENU
        self.previousState = None

    def setState(self, state):
        self.previousState = self.currentState
        self.currentState = state

    def getState(self):
        return self.currentState

    def isMenu(self):
        return self.currentState == GameState.MENU

    def isPlaying(self):
        return self.currentState == GameState.PLAYING

    def isPaused(self):
        return self.currentState == GameState.PAUSED

    def isGameOver(self):
        return self.currentState == GameState.GAME_OVER

    def isBoss(self):
        return self.currentState == GameState.BOSS

    def isVictory(self):
        return self.currentState == GameState.VICTORY
