import pygame as pg
from pygame.locals import *
from pygame.math import Vector2 as Pos
from pygame.rect import Rect
from pygame.color import Color
from pygame.surface import Surface
import random as r

from CommonResources import CommonResources

from Player import Player


class Game :

    def __init__( self, common_resources: CommonResources ) :
        self.common_resources = common_resources
        self.events = self.common_resources.event_holder
        self.colors = self.common_resources.colors
        self.assets = self.common_resources.assets
        self.window = self.common_resources.window

        s = self.window.size
        player_rect = Rect(s.x * 0.45, s.y * 0.92, s.x * 0.1, s.y * 0.025)


        self.player = Player(player_rect, self.colors.random_color().lerp(self.colors.RED, 0.7),
            self.common_resources)

        self.bg = self.colors.BLUE.lerp(self.colors.WHITE, 0.7)


    def check_events( self ) :
        self.player.check_events()


    def render_debug( self, surface: Surface ) :
        ...


    def render( self, surface: Surface ) :
        surface.fill(self.bg)
        self.player.render(surface)

        if self.events.should_render_debug :
            self.render_debug(surface)
