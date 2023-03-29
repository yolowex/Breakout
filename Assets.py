import pygame as pg
from pygame.locals import *
from pygame.math import Vector2 as Pos
from pygame.rect import Rect
from pygame.color import Color
import random as r


class Assets:
    def __init__(self):
        self.font = pg.font.SysFont('Arial',30)
        self.font_monobold = pg.font.SysFont('monospace',30,bold=True)
        self.font_gameover = pg.font.SysFont('sans-serif',60,bold=True)
