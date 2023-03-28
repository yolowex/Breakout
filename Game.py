import pygame as pg
from pygame.locals import *
from pygame.math import Vector2 as Pos
from pygame.rect import Rect
from pygame.color import Color
from pygame.surface import Surface
import random as r

from CommonResources import CommonResources

from Player import Player
from Ball import Ball
from Map import Map

class Game :

    def __init__( self) :

        self.events = CommonResources.event_holder
        self.colors = CommonResources.colors
        self.assets = CommonResources.assets
        self.window = CommonResources.window

        s = self.window.size
        player_rect = Rect(s.x * 0.45, s.y * 0.92, s.x * 0.1, s.y * 0.025)


        self.player = Player(player_rect, self.colors.random_color().lerp(self.colors.RED, 0.7))

        self.map_ = Map("./Maps/map_1.json")

        CommonResources.set_extra_data(self.player,self.map_)

        self.map_.update()

        ball_size = 0.01
        ball_rect = Rect(player_rect.x + player_rect.width / 2 - s.x*ball_size*0.5,
                            player_rect.y - s.x*ball_size,
                            s.x * ball_size,
                            s.x* ball_size)

        self.ball = Ball(ball_rect,self.colors.random_color().lerp(self.colors.BLUE, 0.7))

        self.bg = self.colors.BLUE.lerp(self.colors.WHITE, 0.7)


    def check_events( self ) :
        self.player.check_events()
        self.ball.check_events()
        self.map_.check_events()

    def render_debug( self, surface: Surface ) :
        ...

    def render( self, surface: Surface ) :
        surface.fill(self.bg)
        self.player.render(surface)
        self.ball.render(surface)
        self.map_.render(surface)

        if self.events.should_render_debug :
            self.render_debug(surface)
