import pygame


class FontManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.chineseFontNames = [
            "PingFang SC",
            "STHeiti",
            "Heiti TC",
            "SimHei",
            "Microsoft YaHei",
            "微软雅黑",
            "黑体",
            "STSong",
            "Songti SC",
            "Apple Color Emoji",
        ]
        self.defaultFontName = None
        self._findChineseFont()

    def _findChineseFont(self):
        allFonts = pygame.font.get_fonts()
        for fontName in self.chineseFontNames:
            normalizedName = fontName.lower().replace(" ", "")
            for f in allFonts:
                if normalizedName in f.lower().replace(" ", ""):
                    self.defaultFontName = fontName
                    return

        self.defaultFontName = None

    def getFont(self, size):
        if self.defaultFontName:
            try:
                return pygame.font.SysFont(self.defaultFontName, size)
            except:
                pass
        try:
            return pygame.font.Font(None, size)
        except:
            return pygame.font.SysFont("arial", size)

    def getBoldFont(self, size):
        if self.defaultFontName:
            try:
                return pygame.font.SysFont(self.defaultFontName, size, bold=True)
            except:
                pass
        try:
            return pygame.font.Font(None, size)
        except:
            return pygame.font.SysFont("arial", size, bold=True)
