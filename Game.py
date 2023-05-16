import pygame as pg
from pygame.locals import *
from pygame.math import Vector2 as V2
from pygame.rect import Rect
from pygame.color import Color
from pygame.surface import Surface
import random as r
from typing import Optional
from CommonResources import CommonResources
from Mouse import Mouse
from modules.gui.multiline_text import *

from Colors import Colors
from Player import Player
from Ball import Ball
from Map import Map
from EventHolder import EventHolder
from ui import UI

class Game :

    def __init__( self) :

        self.events = CommonResources.event_holder
        self.colors = CommonResources.colors
        self.assets = CommonResources.assets
        self.window = CommonResources.window
        self.screen_shot: Optional[Surface] = None

        self.ui = UI()

        s = self.window.size
        player_rect = Rect(s.x * 0.45, s.y * 0.92, s.x * 0.1, s.y * 0.025)


        self.player = Player(player_rect, self.colors.random_color().lerp(self.colors.RED, 0.7))

        CommonResources.player = self.player

        self.map_ = Map("./Maps/map_1.json")

        CommonResources.set_extra_data(self.player,self.map_,self)

        self.map_.update()

        ball_size = 0.020
        ball_rect = Rect(player_rect.x + player_rect.width / 2 - s.x*ball_size*0.5,
                            player_rect.y - s.x*ball_size,
                            s.y * ball_size,
                            s.y * ball_size)

        self.ball = Ball(ball_rect,self.colors.random_color().lerp(self.colors.BLUE, 0.7))


    def reload( self,path:str ):
        self.events.game_over = False
        self.map_.reload(path)
        self.player.reset()
        self.ball.reset()

    def get_screen_shot( self ):
        self.screen_shot = self.window.surface.copy()

    def win_text( self ):
        win_text = "شما بردید! برای انتخاب مرحله بعدی کلید اینتر را فشار دهید!"[::-1]
        win_text_english_text = "You win! press enter to proceed!"

        target_font_path = self.assets.persian_font_path
        direction = "rtl"
        font_size = 60
        text = win_text

        if self.events.language == EventHolder.LANGUAGE_ENGLISH :
            target_font_path = self.assets.english_font_path
            direction = "ltr"
            font_size = 30
            text = win_text_english_text

        font = pg.font.SysFont('monospace', 30)
        surface = UltimateMultilineText(text, self.window.size.x * 0.7, font,(150,150,150))

        return surface

    def game_over_text( self ):
        game_over_text = "شما باختید! برای بازی دوباره کلید اینتر را فشار دهید!"[::-1]
        game_over_english_text = "You lose! press enter to play again!"

        target_font_path = self.assets.persian_font_path
        direction = "rtl"
        font_size = 60
        text = game_over_text

        if self.events.language == EventHolder.LANGUAGE_ENGLISH:
            target_font_path = self.assets.english_font_path
            direction = "ltr"
            font_size = 30
            text = game_over_english_text


        font = pg.font.SysFont('monospace',30)
        surface = UltimateMultilineText(text,self.window.size.x*0.7,font,(150,150,150))

        return surface

    def check_events( self ) :
        if not self.events.game_over and not self.events.win:
            self.player.check_events()
            self.ball.check_events()
            self.map_.check_events()

        self.ui.check_events()

        m: Mouse = CommonResources.mouse
        click = CommonResources.event_holder.mouse_pressed_keys[0]

        if K_ESCAPE in self.events.released_keys or self.ui.trigger:
            self.events.should_run_game = False

        text = self.game_over_text()
        rect = text.get_rect()
        rect.center = self.window.rect.center

        if self.events.game_over and (K_RETURN in self.events.pressed_keys or
                                      click and m.rect.colliderect(rect) ):
            self.events.game_over = False
            self.map_.reload()
            self.player.reset()
            self.ball.reset()

        text = self.win_text()
        rect = text.get_rect()
        rect.center = self.window.rect.center
        if self.events.win and (K_RETURN in self.events.pressed_keys or
                                click and m.rect.colliderect(rect) ) :
            self.events.win = False
            self.events.should_run_game = False


    def render_debug( self, surface: Surface ) :
        ...

    def render( self, surface: Surface ) :


        if self.events.game_over :
            surface.blit(self.screen_shot, [0, 0])
            text = self.game_over_text()
            rect = text.get_rect()
            rect.center = self.window.rect.center
            surface.blit(text, rect)

        elif self.events.win:
            surface.blit(self.screen_shot, [0, 0])
            text = self.win_text()
            rect = text.get_rect()
            rect.center = self.window.rect.center
            surface.blit(text, rect)
        else:
            self.map_.render(surface)
            self.player.render(surface)
            self.ball.render(surface)

            if self.events.should_render_debug :
                self.render_debug(surface)

        self.ui.render()
