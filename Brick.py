import pygame as pg
from pygame.locals import *
from pygame.math import Vector2 as Pos
from pygame.rect import Rect
from pygame.color import Color
import random as r
from pygame.surface import Surface

from CommonResources import CommonResources

class Brick:
    def __init__(self,rect:Rect,color:Color,health):
        self.events = CommonResources.event_holder
        self.colors = CommonResources.colors
        self.assets = CommonResources.assets
        self.window = CommonResources.window

        self.rect = rect
        self.color = color

        self.health = health

    @property
    def mfont( self ):
        return self.assets.font.render(f"{self.health}",False,self.colors.WHITE)

    def render_debug( self,surface:Surface ):
        m_rect = self.rect.copy()
        m_rect.width, m_rect.height = self.mfont.get_size()
        m_rect.center = self.rect.center
        surface.blit(self.mfont, m_rect)

    def render( self,surface:Surface ):
        pg.draw.rect(surface,self.color,self.rect)

        if self.events.should_render_debug:
            self.render_debug(surface)
