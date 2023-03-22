import pygame as pg
from pygame.locals import *
from pygame.math import Vector2 as Pos
from pygame.rect import Rect
from pygame.color import Color
import random as r

from Window import Window
from EventHolder import EventHolder
from Colors import Colors
from Assets import Assets
from CommonResources import CommonResources
from Game import Game
from Menu import Menu

pg.init()
window = Window(Pos(800,640))
event_holder = EventHolder()
colors = Colors()
assets = Assets()
common_resources = CommonResources(window,event_holder,assets,colors)

game = Game(common_resources)
menu = Menu(common_resources)
clock = pg.time.Clock()
event_holder.determined_fps = 120

while not event_holder.should_quit:
    event_holder.get_events()
    game.check_events()
    game.render(window.surface)


    pg.display.update()
    clock.tick(event_holder.determined_fps)
    event_holder.final_fps = clock.get_fps()




