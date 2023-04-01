import pygame as pg
from pygame.locals import *
from pygame.math import Vector2 as V2
from pygame.rect import Rect
from pygame.color import Color
import random as r

from Colors import Colors

from pygame.surface import Surface

from EventHolder import EventHolder

from modules.mygame.drawables import TextBox
from modules.mygame.structures import Pos
from CommonResources import CommonResources


class Page :
    def __init__( self, rect: Rect, persian_text_list: list[str],english_text_list: list[str],
            collide_list: list[bool],
            oneliner_list: list[bool] ) :

        self.events = CommonResources.event_holder
        self.colors = CommonResources.colors
        self.assets = CommonResources.assets
        self.window = CommonResources.window

        self.text_color = Colors.BLACK
        self.bg_color = Colors.WHITE
        self.bg_color.a = 185
        self.rect = rect
        self.gap_y = 0.1

        self.persian_text_list = persian_text_list
        self.english_text_list = english_text_list
        self.collide_list = collide_list
        self.oneliner_list = oneliner_list
        self.surface_list: list[pg.surface.Surface] = []
        self.rect_list: list[Rect] = []
        self.persian_font_size = 65
        self.english_font_size = 40

        self.update()
        self.current_collision = None

    def reset( self ):
        self.surface_list.clear()
        self.rect_list.clear()

    def update( self ):
        self.reset()
        self.generate_surfaces()
        self.generate_rects()

    def generate_surfaces( self ) :
        direction = "rtl"
        target_text_list = self.persian_text_list
        target_font_path = self.assets.persian_font_path


        if self.events.language == EventHolder.LANGUAGE_ENGLISH:
            direction = 'ltr'
            target_text_list = self.english_text_list
            target_font_path = self.assets.english_font_path

        size = self.persian_font_size
        if self.events.language == EventHolder.LANGUAGE_ENGLISH:
            size = self.english_font_size

        for text,oneliner in zip(target_text_list,self.oneliner_list) :
            text_box = TextBox(text, Pos(0, 0), self.rect.width, target_font_path, size,
                tuple(Colors.BLACK), tuple(Colors.GLASS), direction, oneliner=oneliner
                ,wholesome=True)
            self.surface_list.append(text_box.text_surface)


    def generate_rects( self ) :
        h = 0
        for ts in self.surface_list :
            self.rect_list.append(Rect(self.rect.x + self.rect.w / 2 - ts.get_width() / 2,
                self.rect.y + self.rect.h / 2 + h, ts.get_width(), ts.get_height()))

            h += ts.get_height()
            h += ts.get_height() * self.gap_y

        for rect in self.rect_list :
            rect.y -= h / 2


    def check_events( self ) :
        m_rect = Rect(0, 0, 2, 2)
        m_rect.x, m_rect.y = self.events.mouse_pos
        m_rect.x -= 1
        m_rect.y -= 1

        self.current_collision = None
        for rect, text, collides, c in zip(self.rect_list, self.persian_text_list, self.collide_list,
                range(len(self.persian_text_list))) :
            if m_rect.colliderect(rect) and collides :
                self.current_collision = c


    def render_debug( self, surface: Surface ) :
        pg.draw.rect(surface, Colors.WHITE, self.rect, width=3)


    def render( self, surface: Surface ) :
        this_surface = Surface(self.rect.size).convert_alpha()
        this_surface.fill(self.bg_color)

        surface.blit(this_surface,self.rect)

        for text_surface, rect in zip(self.surface_list, self.rect_list) :
            surface.blit(text_surface, rect)

        pg.draw.rect(surface, Colors.BLACK, self.rect, width=3)

        if self.events.should_render_debug :
            self.render_debug(surface)
