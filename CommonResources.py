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
    window = None
    event_holder = None
    assets = None
    colors = None
    player = None
    map_ = None

    @staticmethod
    def set_data(window:Window,event_holder:EventHolder,assets:Assets,colors:Colors):
        CommonResources.window = window
        CommonResources.event_holder = event_holder
        CommonResources.assets = assets
        CommonResources.colors = colors
        CommonResources.player = None
        CommonResources.map_ = None


    @staticmethod
    def set_extra_data( player, map_=None ) :
        CommonResources.player = player
        CommonResources.map_ = map_




