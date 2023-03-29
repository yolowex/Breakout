import pygame as pg
from pygame.locals import *
from pygame.math import Vector2 as Pos
from pygame.rect import Rect
from pygame.color import Color
from pygame.surface import Surface
import random as r
from typing import Optional
from CommonResources import CommonResources

from Colors import Colors
from Player import Player
from Ball import Ball
from Map import Map

class Game :

    def __init__( self) :

        self.events = CommonResources.event_holder
        self.colors = CommonResources.colors
        self.assets = CommonResources.assets
        self.window = CommonResources.window
        self.screen_shot: Optional[Surface] = None

        s = self.window.size
        player_rect = Rect(s.x * 0.45, s.y * 0.92, s.x * 0.1, s.y * 0.025)


        self.player = Player(player_rect, self.colors.random_color().lerp(self.colors.RED, 0.7))

        self.map_ = Map("./Maps/map_1.json")

        CommonResources.set_extra_data(self.player,self.map_,self)

        self.map_.update()

        ball_size = 0.01
        ball_rect = Rect(player_rect.x + player_rect.width / 2 - s.x*ball_size*0.5,
                            player_rect.y - s.x*ball_size,
                            s.x * ball_size,
                            s.x* ball_size)

        self.ball = Ball(ball_rect,self.colors.random_color().lerp(self.colors.BLUE, 0.7))

        self.bg = self.colors.BLUE.lerp(self.colors.WHITE, 0.7)

    def get_screen_shot( self ):
        self.screen_shot = self.window.surface.copy()

    def game_over_text( self ):
        game_over_text = "You lose , press F to try again"
        s = self.assets.font_gameover.size(game_over_text)
        surface = Surface([s[0]*1.1,s[1]*2.5]).convert_alpha()
        color = Colors.WHITE
        color.a = 155
        surface.fill(color)

        rect = surface.get_rect()
        text = self.assets.font_gameover.render(game_over_text,True,[0,0,0])

        rect_2 = text.get_rect()
        rect_2.center = rect.center

        surface.blit(text,rect_2)

        return surface

    def check_events( self ) :
        if not self.events.game_over:
            self.player.check_events()
            self.ball.check_events()
            self.map_.check_events()

        if self.events.game_over and K_f in self.events.pressed_keys:
            self.events.game_over = False
            self.map_.reload()
            self.player.reset()
            self.ball.reset()


    def render_debug( self, surface: Surface ) :
        ...

    def render( self, surface: Surface ) :
        if not self.events.game_over:
            surface.fill(self.bg)
            self.player.render(surface)
            self.ball.render(surface)
            self.map_.render(surface)

            if self.events.should_render_debug :
                self.render_debug(surface)
        else:
            surface.blit(self.screen_shot,[0,0])
            text = self.game_over_text()
            rect = text.get_rect()
            rect.center = self.window.rect.center
            surface.blit(text,rect)
