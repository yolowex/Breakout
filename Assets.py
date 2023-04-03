import pygame as pg
from pygame.locals import *
from pygame.math import Vector2 as Pos
from pygame.rect import Rect
from pygame.color import Color
import random as r


class Assets:
    def __init__(self):
        self.font = pg.font.SysFont('Arial',30)
        self.font_monobold = pg.font.SysFont('monospace',30,bold=True)
        self.font_gameover = pg.font.SysFont('Arial',30,bold=True)
        self.persian_font_path = "./fonts/farsi/farsi 3.ttf"
        self.english_font_path = "./fonts/english/FreeMonoBold.ttf"

        self.bad_sound = pg.mixer.Sound("./sounds/bad_bonus.wav")
        self.good_sound = pg.mixer.Sound("./sounds/Fruit collect 1.wav")
        self.best_sound = pg.mixer.Sound("./sounds/Big Egg collect 1.wav")

        self.hit_sounds = [pg.mixer.Sound("./sounds/" + i + ".wav") for i in
            ["hit1", "hit2", "hit3", "hit4", "hit5"]]

        self.gun_sounds = [pg.mixer.Sound("./sounds/" + i + ".wav") for i in
            [f"laserShoot{i}" for i in range(1,4)]]

        self.shoot_hit_sounds = [pg.mixer.Sound("./sounds/" + i + ".wav") for i in
            [f"shoot_hit{i}" for i in range(1, 6)]]

        self.break_sounds = [pg.mixer.Sound("./sounds/" + i + ".wav") for i in
            [f"hitHurt{i}" for i in range(1, 5)]]