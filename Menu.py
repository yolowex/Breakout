import pygame as pg
from pygame.locals import *
from pygame.math import Vector2 as V2
from pygame.rect import Rect
from pygame.color import Color
import random as r

from Colors import Colors

import sys
from pygame.surface import Surface

from modules.mygame.drawables import TextBox
from modules.mygame.structures import Pos

from CommonResources import CommonResources

from Page import Page

class Menu:

    MAIN_MENU = 0
    LEVEL_MENU = 1
    SETTINGS_MENU = 2
    ABOUT_US = 3
    EXIT = 4

    def __init__( self ) :
        self.events = CommonResources.event_holder
        self.colors = CommonResources.colors
        self.assets = CommonResources.assets
        self.window = CommonResources.window

        self.bg = Colors.BLUE.lerp(Colors.BLACK,0.7).lerp(Colors.GRAY,0.3)

        self.page_menu = ...
        self.level_menu = ...
        self.page_settings = ...
        self.page_about_us = ...
        self.page_exit = ...

        self.page_dict = {}

        self.page_number = Menu.MAIN_MENU

        self.make_pages()

    def make_pages( self ):
        self.make_page_0()
        self.make_page_1()
        self.make_page_2()
        self.make_page_3()
        self.make_page_4()

        self.page_dict = {
            Menu.MAIN_MENU: self.page_menu,
            Menu.LEVEL_MENU: self.level_menu,
            Menu.SETTINGS_MENU: self.page_settings,
            Menu.ABOUT_US: self.page_about_us,
            Menu.EXIT: self.page_exit
        }

    def make_page_0( self ):
        t0 = "آجر شکن حرفه ای!"
        t1 = "شروع بازی"
        t2 = "تنظیمات"
        t3 = "درباره ما"
        t4 = "خروج"

        text_list = [t0, t1, t2, t3, t4]
        collide_list = [bool(i) for i in [0, 1, 1, 1, 1]]
        oneliner_list = [bool(i) for i in [1, 1, 1, 1, 1]]

        s = self.window.size
        rect = Rect([s.x * 0.1, s.y * 0.1, s.x * 0.65, s.y * 0.8])

        self.page_menu = Page(rect, text_list, collide_list,oneliner_list)


    def make_page_1( self ):
        ...

    def make_page_2( self ):
        ...

    def make_page_3( self ):
        t0 = "این بازی برای دوره آموزش پروژه محور کتابخانه پایگیم در سایت تاپلرن"\
             " توسط مدرس محمد معین آذری طراحی و تولید شده است."

        t1 = "بازگشت"


        text_list = [t0, t1]
        collide_list = [bool(i) for i in [0, 1]]
        oneliner_list = [bool(i) for i in [0, 1]]

        s = self.window.size
        rect = Rect([s.x * 0.1, s.y * 0.1, s.x * 0.8, s.y * 0.8])

        self.page_about_us = Page(rect, text_list, collide_list, oneliner_list)

    def make_page_4( self ):
        t0 = "آیا مطمئنید میخواهید از بازی خارج شوید؟"
        t1 = "بله"
        t2 = "خیر"


        text_list = [t0, t1, t2]
        collide_list = [bool(i) for i in [0, 1, 1]]
        oneliner_list = [bool(i) for i in [0, 1, 1]]

        s = self.window.size
        rect = Rect([s.x * 0.01, s.y * 0.15, s.x * 0.98, s.y * 0.7])

        self.page_exit = Page(rect, text_list, collide_list,oneliner_list)


    @property
    def current_page( self ) -> Page:
        return self.page_dict[self.page_number]

    def check_events( self ):
        self.current_page.check_events()

        if self.current_page.current_collision is not None and self.events.mouse_pressed_keys[0]:
            c = self.current_page.current_collision
            if self.page_number == Menu.MAIN_MENU:
                if c == 1:
                    print('it\'s game!')
                    self.page_number = Menu.LEVEL_MENU

                elif c == 2:
                    print('it\'s settings!')
                    self.page_number = Menu.SETTINGS_MENU

                elif c == 3:
                    print('it\'s me!')
                    self.page_number = Menu.ABOUT_US

                elif c == 4:
                    print('it\'s exit!')
                    self.page_number = Menu.EXIT


            elif self.page_number == Menu.LEVEL_MENU:
                ...
            elif self.page_number == Menu.SETTINGS_MENU:
                ...
            elif self.page_number == Menu.ABOUT_US:
                if c == 1:
                    self.page_number = Menu.MAIN_MENU

            elif self.page_number == Menu.EXIT:
                if c == 1:
                    self.events.should_quit = True

                elif c == 2:
                    self.page_number = Menu.MAIN_MENU



    def render_debug( self,surface:Surface ):
        ...

    def render( self,surface:Surface  ):
        surface.fill(self.bg)
        self.current_page.render(surface)

        if self.events.should_render_debug:
            self.render_debug(surface)

