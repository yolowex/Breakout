import pygame as pg
from pygame.locals import *
from pygame.math import Vector2 as Pos
from pygame.rect import Rect
from pygame.color import Color
from pygame.surface import Surface
import random as r


class EventHolder:
    def __init__(self):
        self.pressed_keys = []
        self.released_keys = []
        self.held_keys = []

        self.mouse_pos = Pos(0,0)
        self.mouse_pressed_keys = [False,False,False]
        self.mouse_released_keys = [False,False,False]
        self.mouse_held_keys = [False,False,False]
        self.mouse_focus = False

        self.should_render_debug = False
        self.should_run_game = False
        self.should_quit = False


    def get_events( self ):
        self.pressed_keys.clear()
        self.mouse_pressed_keys.clear()
        self.released_keys.clear()
        self.mouse_released_keys.clear()


        for i in pg.event.get():
            if i.type == QUIT or i.type == KEYDOWN and i.key == K_ESCAPE:
                self.should_quit = True

            if i.type == KEYDOWN:
                self.pressed_keys.append(i.key)

            if i.type == KEYUP:
                self.released_keys.append(i.key)

            if i.type == MOUSEBUTTONDOWN:
                self.mouse_pressed_keys = list(pg.mouse.get_pressed())
                self.mouse_held_keys = list(pg.mouse.get_pressed())

            if i.type == MOUSEBUTTONUP:
                self.mouse_released_keys = list(pg.mouse.get_pressed())
                self.mouse_held_keys = list(pg.mouse.get_pressed())

