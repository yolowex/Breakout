import pygame as pg
from pygame.locals import *
from pygame.math import Vector2 as Pos
from pygame.rect import Rect
from pygame.color import Color
import random as r

from Window import Window
from EventHolder import EventHolder
from Assets import Assets
from Colors import Colors

class CommonResources:
    def __init__(self,window:Window,event_holder:EventHolder,assets:Assets,colors:Colors):
        self.window = window
        self.event_holder = event_holder
        self.assets = assets
        self.colors = colors