import traceback
import sys
import re

try:



    import pygame as pg
    from pygame.locals import *
    from pygame.math import Vector2 as V2
    from pygame.rect import Rect
    from pygame.color import Color
    import random as r
    import sys
    import json
    import math

    try:
        def version():
            v = pg.version
            return f"SDL version: {v.SDL}, pygame version: {v.ver}, python version: {sys.version}"

        print("[CHECKPOINT: Version] :", version())
    except Exception as e:
        print("[CHECKPOINT: Version] : Could not print Pygame's version",e)

    from Window import Window
    from EventHolder import EventHolder
    from Colors import Colors
    from Assets import Assets
    from CommonResources import CommonResources
    from Game import Game
    from Menu import Menu
    from Mouse import Mouse
    # from modules.mygame.drawables import TextBox,TextView
    # from modules.mygame.structures import *
    from functions import *


    pg.init()
    scale = 50
    ar = aspect_ratio = V2(9,18)
    rsize = V2(ar.x*scale,ar.y*scale)
    window = Window(rsize)

    event_holder = EventHolder()
    colors = Colors()
    assets = Assets()
    common_resources = CommonResources.set_data(window,event_holder,assets,colors)

    window.surface.fill([255,255,255])
    loading = assets.font_monobold.render("Please wait while Loading...",True,(0,0,0))
    c = Pos(window.rect.center)
    c.x -= loading.get_width()/2
    c.y -= loading.get_height()/2

    window.surface.blit(loading,c)

    pg.display.update()


    game = Game()
    menu = Menu()
    mouse = Mouse()
    CommonResources.mouse = mouse

    f = pg.font.SysFont('monospace',30,bold=True)

    font = lambda: f.render(f"FPS:{round(event_holder.final_fps)}",False,[80,12,25])


    event_holder.determined_fps = 125
    event_holder.menu_fps = 60


    while not event_holder.should_quit:
        event_holder.get_events()

        if event_holder.should_run_game:
            game.check_events()
            game.render(window.surface)
        else:
            menu.check_events()
            menu.render(window.surface)

        mouse.check_events()
        mouse.render(window.surface)


        if K_F3 in event_holder.pressed_keys:
            event_holder.should_render_debug = not event_holder.should_render_debug

        if K_F2 in event_holder.pressed_keys:
            event_holder.is_dev = not event_holder.is_dev

        if event_holder.should_render_debug:
            window.surface.blit(font(),[0,0])

        pg.display.update()

        fps = event_holder.determined_fps
        if not event_holder.should_run_game:
            fps = event_holder.menu_fps


except Exception as e:
    error_message = re.sub(r'\s+', ' ', traceback.format_exc())
    print("[Checkpoint:Error]", error_message.strip())
    print("[Checkpoint:Error]", traceback.format_exc())
