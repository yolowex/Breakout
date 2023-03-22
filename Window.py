import pygame as pg
from pygame.locals import *
from pygame.math import Vector2 as Pos
from pygame.rect import Rect
from pygame.color import Color
import random as r


class Window:
    def __init__(self,size:Pos):
        self.size = size
        self.surface = pg.display.set_mode(size,SCALED | FULLSCREEN)



