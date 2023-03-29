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

from Page import Page

class Menu:

    def __init__( self ) :
        self.events = CommonResources.event_holder
        self.colors = CommonResources.colors
        self.assets = CommonResources.assets
        self.window = CommonResources.window

        self.bg = Colors.BLUE.lerp(Colors.BLACK,0.7).lerp(Colors.GRAY,0.3)

        collide_list = []

        t1 = "شروع بازی"
        t2 = "تنظیمات"
        t3 = "درباره ما"
        t4 = "خروج"

        text_list = [ t1,t2,t3,t4 ]

        s = self.window.size
        rect = Rect([s.x*0.1,s.y*0.1,s.x*0.65,s.y*0.8])

        self.page = Page(rect,text_list,collide_list)





    def check_events( self ):
        self.page.check_events()

    def render_debug( self,surface:Surface ):
        ...

    def render( self,surface:Surface  ):
        surface.fill(self.bg)
        self.page.render(surface)

        if self.events.should_render_debug:
            self.render_debug(surface)

