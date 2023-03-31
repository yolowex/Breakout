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
from functions import *

from Page import Page
import json
from Video import Video

file = open("./Maps/all_maps.json").read()

all_maps:dict = json.loads(file)
root = "./Maps/"
all_maps = {int(key):root+value for key,value in all_maps.items()}


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
        self.game = CommonResources.game

        self.bg = Colors.BLUE.lerp(Colors.BLACK,0.7).lerp(Colors.GRAY,0.9)

        self.page_menu = ...
        self.page_level = ...
        self.page_settings = ...
        self.page_about_us = ...
        self.page_exit = ...

        self.page_dict = {}

        self.page_number = Menu.MAIN_MENU


        size_scale = Pos(0.5,0.5)
        s = self.window.size
        size = Pos(s.x*size_scale.x,s.y*size_scale.y)


        self.videos_x_pos = 0
        self.videos_direction = -1
        self.video_0 = Video("./videos/1.mp4",size_scale)
        self.video_1 = Video("./videos/2.mp4",size_scale)
        self.video_2 = Video("./videos/3.mp4",size_scale)
        self.video_3 = Video("./videos/4.mp4",size_scale)
        self.video_4 = Video("./videos/5.mp4",size_scale)
        self.video_5 = Video("./videos/6.mp4",size_scale)

        self.videos = [
            self.video_0,
            self.video_1,
            self.video_2,
            self.video_3,
            self.video_4,
            self.video_5,
        ]

        self.video_0.pos = Pos(0,0)
        self.video_1.pos = Pos(size.x,0)
        self.video_2.pos = Pos(0,size.y)
        self.video_3.pos = Pos(size.x,size.y)
        self.video_4.pos = Pos(size.x*2,size.y)
        self.video_5.pos = Pos(size.x*2,0)




        self.video_index = 0


        self.make_pages()


    def relang( self ):
        self.events.language *=-1
        for i in self.page_dict:
            page = self.page_dict[i]
            if isinstance(page,Page):
                page.update()

    def update_dict( self ):
        self.page_dict = {Menu.MAIN_MENU : self.page_menu, Menu.LEVEL_MENU : self.page_level,
            Menu.SETTINGS_MENU : self.page_settings, Menu.ABOUT_US : self.page_about_us,
            Menu.EXIT : self.page_exit}

    def make_pages( self ):
        self.make_page_0()
        self.make_page_1()
        self.make_page_2()
        self.make_page_3()
        self.make_page_4()
        self.update_dict()



    def make_page_0( self ):
        t0 = "آجر شکن حرفه ای!"
        t1 = "شروع بازی"
        t2 = "تنظیمات"
        t3 = "درباره ما"
        t4 = "خروج"

        e0 = "Breakout Pro!"
        e1 = "Play Game"
        e2 = "Settings"
        e3 = "About us"
        e4 = "Exit"


        text_list = [t0, t1, t2, t3, t4]
        english_text_list = [e0,e1,e2,e3,e4]

        collide_list = [bool(i) for i in [0, 1, 1, 1, 1]]
        oneliner_list = [bool(i) for i in [1, 1, 1, 1, 1]]

        s = self.window.size
        rect = Rect([s.x * 0.1, s.y * 0.1, s.x * 0.65, s.y * 0.8])

        self.page_menu = Page(rect, text_list,english_text_list, collide_list,oneliner_list)
        self.page_menu.gap_y = 0.5
        self.page_menu.update()


    @property
    def level_english_text( self ):
        text = f"Level {self.events.current_level}"
        return text

    @property
    def level_persian_text( self ) :
        text = "مرحله "
        text += f"{self.events.current_level}"
        return text


    def make_page_1( self ):
        t0 = self.level_persian_text
        t1 = "مرحله بعد"
        t2 = "مرحله قبل"
        t3 = "شروع بازی"
        t4 = "بازگشت"

        e0 = self.level_english_text
        e1 = "Next Level"
        e2 = "Previous Level"
        e3 = "Play"
        e4 = "Back"

        text_list = [t0, t1, t2, t3, t4]
        english_text_list = [e0, e1, e2, e3, e4]

        collide_list = [bool(i) for i in [0, 1, 1, 1, 1]]
        oneliner_list = [bool(i) for i in [1, 1, 1, 1, 1]]

        s = self.window.size
        rect = Rect([s.x * 0.1, s.y * 0.1, s.x * 0.75, s.y * 0.60])

        self.page_level = Page(rect, text_list, english_text_list, collide_list, oneliner_list)
        self.page_level.gap_y = 0.5
        self.page_level.update()

    def make_page_2( self ):

        t0 = "تنظیمات"
        t1 = "زبان: فارسی"
        t2 = "بازگشت"

        e0 = "Settings"
        e1 = "Language: English"
        e2 = "Back"

        text_list = [t0, t1, t2]
        english_text_list = [e0,e1,e2]

        collide_list = [bool(i) for i in [0, 1, 1]]
        oneliner_list = [bool(i) for i in [1, 1, 1]]

        s = self.window.size
        rect = Rect([s.x * 0.1, s.y * 0.4, s.x * 0.8, s.y * 0.4])

        self.page_settings = Page(rect, text_list,english_text_list, collide_list, oneliner_list)
        self.page_settings.gap_y = 0.7
        self.page_settings.update()

    def make_page_3( self ):
        t0 = "این بازی برای دوره آموزش پروژه محور کتابخانه پایگیم در سایت تاپلرن"\
             " توسط مدرس محمد معین آذری طراحی و تولید شده است."

        t1 = "بازگشت"

        e0 = "This game was made by mohammad moein azari." \
             " This project" \
            " resides at: github.com/mmdmoa/Breakout ."
        e1 = "Back"

        text_list = [t0, t1]
        english_text_list = [e0,e1]

        collide_list = [bool(i) for i in [0, 1]]
        oneliner_list = [bool(i) for i in [0, 1]]

        s = self.window.size
        rect = Rect([s.x * 0.1, s.y * 0.1, s.x * 0.8, s.y * 0.8])

        self.page_about_us = Page(rect, text_list,english_text_list, collide_list, oneliner_list)

    def make_page_4( self ):
        t0 = "آیا مطمئنید میخواهید از بازی خارج شوید؟ "
        t1 = "بله"
        t2 = "خیر"

        e0 = "Are you sure you are willing to give up and leave the game?"
        e1 = "Yes"
        e2 = "No way, i\'m in"


        text_list = [t0, t1, t2]
        english_text_list = [e0,e1,e2]

        collide_list = [bool(i) for i in [0, 1, 1]]
        oneliner_list = [bool(i) for i in [0, 1, 1]]

        s = self.window.size
        rect = Rect([s.x * 0.01, s.y * 0.15, s.x * 0.98, s.y * 0.7])

        self.page_exit = Page(rect, text_list,english_text_list, collide_list,oneliner_list)

    @property
    def current_level_path( self ):
        return all_maps[self.events.current_level]

    def reverse( self ):
        self.videos_direction *= -1

    @property
    def current_page( self ) -> Page:
        return self.page_dict[self.page_number]

    def check_events( self ):


        for video in self.videos:
            video.pos.x += self.videos_direction
            if video.pos.x<=-video.size.x:
                video.pos.x+=video.size.x*3
            if video.pos.x>self.window.size.x:
                video.pos.x-=video.size.x*3

        self.current_page.check_events()

        self.video_0.check_events()
        self.video_1.check_events()
        self.video_2.check_events()
        self.video_3.check_events()
        self.video_4.check_events()
        self.video_5.check_events()


        if K_F1 in self.events.released_keys:
            self.events.should_quit = True

        if K_ESCAPE in self.events.released_keys:
            if self.page_number not in [Menu.MAIN_MENU,Menu.EXIT]:
                self.page_number = Menu.MAIN_MENU
            elif self.page_number == Menu.MAIN_MENU:
                self.page_number = Menu.EXIT
            elif self.page_number == Menu.EXIT:
                self.events.should_quit = True

        elif self.current_page.current_collision is not None and self.events.mouse_pressed_keys[0]:
            c = self.current_page.current_collision

            if self.page_number == Menu.MAIN_MENU:
                if c == 1:
                    self.page_number = Menu.LEVEL_MENU

                elif c == 2:
                    self.page_number = Menu.SETTINGS_MENU

                elif c == 3:
                    self.page_number = Menu.ABOUT_US

                elif c == 4:
                    self.page_number = Menu.EXIT


            elif self.page_number == Menu.LEVEL_MENU:
                if c == 1:
                    next_level = self.events.current_level + 1
                    if next_level in all_maps:
                        self.events.current_level = next_level
                        self.make_page_1()
                        self.page_level.update()
                        self.update_dict()
                elif c == 2:
                    next_level = self.events.current_level - 1

                    if next_level in all_maps:
                        self.events.current_level = next_level
                        self.make_page_1()
                        self.page_level.update()
                        self.update_dict()
                elif c == 3:
                    self.events.should_run_game = True
                    self.game.reload(self.current_level_path)
                elif c == 4:
                    self.reverse()
                    self.page_number = Menu.MAIN_MENU


            elif self.page_number == Menu.SETTINGS_MENU:

                if c == 1:
                    self.relang()
                elif c == 2:
                    self.reverse()
                    self.page_number = Menu.MAIN_MENU

            elif self.page_number == Menu.ABOUT_US:
                self.reverse()

                if c == 1:
                    self.page_number = Menu.MAIN_MENU

            elif self.page_number == Menu.EXIT:
                if c == 1:
                    self.events.should_quit = True

                elif c == 2:
                    self.page_number = Menu.MAIN_MENU



    def render_debug( self,surface:Surface ):
        ...

    def render_videos( self,surface:Surface  ):
        pos = Pos(self.videos_x_pos,0)
        self.video_0.render(surface,pos)
        self.video_1.render(surface,pos)
        self.video_2.render(surface,pos)
        self.video_3.render(surface,pos)
        self.video_4.render(surface,pos)
        self.video_5.render(surface,pos)



    def render( self,surface:Surface  ):
        surface.fill(self.bg)

        self.render_videos(surface)

        self.current_page.render(surface)

        if self.events.should_render_debug:
            self.render_debug(surface)

