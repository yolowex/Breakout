import pygame as pg
from pygame.locals import *
from pygame.math import Vector2 as Pos
from pygame.rect import Rect
from pygame.color import Color
import random as r
from pygame.surface import Surface


class Brick:
    def __init__(self,rect:Rect,color:Color):
        self.rect = rect
        self.color = color

    def render( self,surface:Surface ):
        pg.draw.rect(surface,self.color,self.rect)