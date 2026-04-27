import pygame
import os
import sys


class FontManager:
    _instance = None
    _fontCache = {}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._defaultFontPath = None
        self._findChineseFontPath()

    def _findChineseFontPath(self):
        fontPaths = []

        if sys.platform == "darwin":
            macFontPaths = [
                "/System/Library/Fonts/PingFang.ttc",
                "/System/Library/Fonts/STHeiti Light.ttc",
                "/System/Library/Fonts/STHeiti Medium.ttc",
                "/System/Library/Fonts/Hiragino Sans GB.ttc",
                "/System/Library/Fonts/Supplemental/Songti.ttc",
                "/System/Library/Fonts/Supplemental/STHeiti Light.ttc",
                "/System/Library/Fonts/Apple Braille Outline 6 Dot.ttf",
            ]
            fontPaths.extend(macFontPaths)

            home = os.path.expanduser("~")
            userFontPaths = [
                os.path.join(home, "Library", "Fonts", "PingFang.ttc"),
                os.path.join(home, "Library", "Fonts", "Microsoft YaHei.ttf"),
                os.path.join(home, "Library", "Fonts", "SimHei.ttf"),
            ]
            fontPaths.extend(userFontPaths)

        elif sys.platform == "win32":
            winFontPaths = [
                "C:\\Windows\\Fonts\\msyh.ttc",
                "C:\\Windows\\Fonts\\msyhbd.ttc",
                "C:\\Windows\\Fonts\\simhei.ttf",
                "C:\\Windows\\Fonts\\simsun.ttc",
            ]
            fontPaths.extend(winFontPaths)

        elif sys.platform.startswith("linux"):
            linuxFontPaths = [
                "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
                "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
                "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
                "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
            ]
            fontPaths.extend(linuxFontPaths)

        for fontPath in fontPaths:
            if os.path.exists(fontPath):
                try:
                    testFont = pygame.font.Font(fontPath, 24)
                    testSurface = testFont.render("测试中文雷电", True, (255, 255, 255))
                    self._defaultFontPath = fontPath
                    return
                except:
                    continue

        self._defaultFontPath = None

    def getFont(self, size):
        cacheKey = f"font_{size}"
        if cacheKey in FontManager._fontCache:
            return FontManager._fontCache[cacheKey]

        if self._defaultFontPath:
            try:
                font = pygame.font.Font(self._defaultFontPath, size)
                FontManager._fontCache[cacheKey] = font
                return font
            except:
                pass

        try:
            font = pygame.font.Font(None, size)
            FontManager._fontCache[cacheKey] = font
            return font
        except:
            font = pygame.font.SysFont("arial", size)
            FontManager._fontCache[cacheKey] = font
            return font

    def getBoldFont(self, size):
        cacheKey = f"bold_{size}"
        if cacheKey in FontManager._fontCache:
            return FontManager._fontCache[cacheKey]

        if self._defaultFontPath:
            try:
                font = pygame.font.Font(self._defaultFontPath, size)
                FontManager._fontCache[cacheKey] = font
                return font
            except:
                pass

        try:
            font = pygame.font.Font(None, size)
            FontManager._fontCache[cacheKey] = font
            return font
        except:
            font = pygame.font.SysFont("arial", size, bold=True)
            FontManager._fontCache[cacheKey] = font
            return font

    def hasChineseFont(self):
        return self._defaultFontPath is not None
