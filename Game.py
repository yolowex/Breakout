import pygame as pg
from pygame.locals import *
from pygame.math import Vector2 as Pos
from pygame.rect import Rect
from pygame.color import Color
from pygame.surface import Surface
import random as r

from CommonResources import CommonResources

class Game:
    def __init__(self,common_resources:CommonResources):
        self.common_resources = common_resources
        self.events = self.common_resources.event_holder
        self.colors = self.common_resources.colors
        self.assets = self.common_resources.assets
        self.window = self.common_resources.window


        self.bg = self.colors.BLUE.lerp(self.colors.WHITE,0.7)

    def check_events( self ):
        ...

    def render_debug( self,surface: Surface):
        ...

    def render( self,surface: Surface ):
        surface.fill(self.bg)


        if self.events.should_render_debug:
            self.render_debug(surface)