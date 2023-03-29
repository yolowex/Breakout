import pygame as pg
from pygame.locals import *
from pygame.math import Vector2 as Pos
from pygame.rect import Rect
from pygame.color import Color
import random as r
import sys
import json


from Window import Window
from EventHolder import EventHolder
from Colors import Colors
from Assets import Assets
from CommonResources import CommonResources
from Game import Game
from Menu import Menu







# if r.choice([1]): sys.exit()

pg.init()
window = Window(Pos(800,800))
event_holder = EventHolder()
colors = Colors()
assets = Assets()
common_resources = CommonResources.set_data(window,event_holder,assets,colors)

game = Game()
menu = Menu()

f = pg.font.SysFont('monospace',30,bold=True)
font = lambda: f.render(f"FPS:{round(event_holder.final_fps)}",False,[80,12,25])

clock = pg.time.Clock()
event_holder.determined_fps = 120

while not event_holder.should_quit:
    event_holder.get_events()
    game.check_events()
    game.render(window.surface)

    if K_F3 in event_holder.pressed_keys:
        event_holder.should_render_debug = not event_holder.should_render_debug

    if event_holder.should_render_debug:
        window.surface.blit(font(),[0,0])


    pg.display.update()
    clock.tick(event_holder.determined_fps)
    event_holder.final_fps = clock.get_fps()




