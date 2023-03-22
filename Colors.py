import pygame as pg
from pygame.locals import *
from pygame.math import Vector2 as Pos
from pygame.rect import Rect
from pygame.color import Color
import random as r


class Colors:
    @staticmethod
    def random_color():
        return Color([r.randint(0,255) for _ in range(3)])

    def __init__(self):
        self.RED = Color(255,0,0)
        self.GREEN = Color(0,255,0)
        self.BLUE = Color(0,0,255)
        self.GLASS = Color(0,0,0,0)
        self.WHITE = Color(255,255,255)
        self.GRAY = Color(127,127,127)
        self.BLACK = Color(0,0,0)

