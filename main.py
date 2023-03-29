import pygame as pg
from pygame.locals import *
from pygame.math import Vector2 as Pos
from pygame.rect import Rect
from pygame.color import Color
import random as r
import sys
import json
import math

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

def rotate(origin, point, angle):
    angle = math.radians(angle)
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

pg.mouse.set_visible(False)
mouse_color = pg.color.Color(0,0,0)
mouse_radius = 15
mouse_width = 1
mouse_angle = 0

def top(angle=0):
    pos = event_holder.mouse_pos.copy()
    pos.y -= mouse_radius

    pos = Pos(rotate(event_holder.mouse_pos,pos,angle))

    return pos

def lines(angle):
    p1 = top(90+angle)
    p2 = top(180+angle)
    p3 = top(270+angle)
    p4 = top(360+angle)

    return (p1,p3),(p2,p4)

while not event_holder.should_quit:
    event_holder.get_events()
    game.check_events()
    game.render(window.surface)



    if K_F3 in event_holder.pressed_keys:
        event_holder.should_render_debug = not event_holder.should_render_debug

    if event_holder.should_render_debug:
        window.surface.blit(font(),[0,0])


    if event_holder.mouse_focus:
        mouse_angle += 1

        pg.draw.circle(window.surface,[0,0,0],event_holder.mouse_pos
            ,mouse_radius,width=mouse_width)

        line_a,line_b = lines(mouse_angle)
        pg.draw.line(window.surface,[0,0,0],line_a[0],line_a[1])
        pg.draw.line(window.surface,[0,0,0],line_b[0],line_b[1])



    pg.display.update()
    clock.tick(event_holder.determined_fps)
    event_holder.final_fps = clock.get_fps()




