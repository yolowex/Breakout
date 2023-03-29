import pygame as pg
from pygame.locals import *
from pygame.math import Vector2 as V2
from pygame.rect import Rect
from pygame.color import Color
import random as r

from Colors import Colors

from pygame.surface import Surface

from modules.mygame.drawables import TextBox
from modules.mygame.structures import Pos

from CommonResources import CommonResources


class Page :
    LANGUAGE_PERSIAN = 0
    LANGUAGE_ENGLISH = 1


    def __init__( self, rect: Rect, text_list: list[str], collide_list: list[bool],
            oneliner_list: list[bool] ) :

        self.events = CommonResources.event_holder
        self.colors = CommonResources.colors
        self.assets = CommonResources.assets
        self.window = CommonResources.window

        self.rect = rect
        self.gap_y = 0.1

        self.text_list = text_list
        self.collide_list = collide_list
        self.oneliner_list = oneliner_list
        self.surface_list: list[pg.surface.Surface] = []
        self.rect_list: list[Rect] = []
        self.persian_font_path = "./fonts/farsi/farsi 512.ttf"
        self.english_font_path = "./english"
        self.language = Page.LANGUAGE_PERSIAN

        self.generate_surfaces()
        self.generate_rects()
        self.current_collision = None


    def generate_surfaces( self ) :
        for text,oneliner in zip(self.text_list,self.oneliner_list) :
            text_box = TextBox(text, Pos(0, 0), self.rect.width, self.persian_font_path, 60,
                tuple(Colors.WHITE), tuple(Colors.BLACK), "rtl", oneliner=oneliner)
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
        for rect, text, collides, c in zip(self.rect_list, self.text_list, self.collide_list,
                range(len(self.text_list))) :
            if m_rect.colliderect(rect) and collides :
                self.current_collision = c


    def render_debug( self, surface: Surface ) :
        pg.draw.rect(surface, Colors.WHITE, self.rect, width=3)


    def render( self, surface: Surface ) :
        for text_surface, rect in zip(self.surface_list, self.rect_list) :
            surface.blit(text_surface, rect)

        if self.events.should_render_debug :
            self.render_debug(surface)
