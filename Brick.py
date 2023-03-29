import pygame as pg
from pygame.locals import *
from pygame.math import Vector2 as Pos
from pygame.rect import Rect
from pygame.color import Color
import random as r
from pygame.surface import Surface
from Bonus import Bonus

from Colors import Colors
from CommonResources import CommonResources

class Brick:
    def __init__(self,rect:Rect,color:Color,health):
        self.events = CommonResources.event_holder
        self.colors = CommonResources.colors
        self.assets = CommonResources.assets
        self.window = CommonResources.window

        self.rect = rect
        self.color = color
        self.bonus = None
        self.health = health

    @property
    def mfont( self ):
        return self.assets.font.render(f"{self.health}",False,self.colors.WHITE)


    def set_bonus( self,chance_percent:int ):
        l = [0] * (100-chance_percent)
        l += [1] * chance_percent
        if r.choice(l):
            bonus_name = r.choice(Bonus.names_list)
            self.bonus = Bonus(bonus_name,
                self.rect.center,
                min([self.rect.width,self.rect.height])/4,
                Bonus.all_[bonus_name]
            )


    def render_debug( self,surface:Surface ):
        m_rect = self.rect.copy()
        m_rect.width, m_rect.height = self.mfont.get_size()
        m_rect.center = self.rect.center
        surface.blit(self.mfont, m_rect)

    def render( self,surface:Surface ):
        rect = self.rect.copy()

        rect.x-=1
        rect.y-=1
        rect.w+=1
        rect.h+=1

        pg.draw.rect(surface,self.color,rect)
        pg.draw.rect(surface,self.color.lerp(Colors.BLACK,0.5),rect,width=3)

        if self.events.should_render_debug:
            self.render_debug(surface)
