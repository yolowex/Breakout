import pygame as pg
from pygame.locals import *
from pygame.math import Vector2 as Pos
from pygame.rect import Rect
from pygame.color import Color
import random as r

from typing import Optional
from Window import Window
from EventHolder import EventHolder
from Assets import Assets
from Colors import Colors


class CommonResources:
    window:Optional[Window] = None
    event_holder:Optional[EventHolder] = None
    assets:Optional[Assets] = None
    colors:Optional[Colors] = None
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




