import pygame as pg
from pygame import Vector2
from pygame.locals import *
from modules.mygame.drawables import TextBox


pg.init()
screen = pg.display.set_mode([800, 600], SCALED)
font_path = "../fonts/farsi/farsi 1.ttf"
font = pg.Font(font_path, 35)

text = "ما یه مشت سربازیم جون به کف\nعزرائیل با اکیپ ما جوره پس"
text+="\n"
text += "کمک کار همیم حتی با پول کم"
text+="\n"
text+="طعم رپمو مزه کن شوره نه؟"

pg_surface = font.render(text, True, "black")
pg_rect = pg_surface.get_rect(bottom=screen.get_height() / 2, centerx=screen.get_width() / 2)

text_box = TextBox(text.replace("\n","/"), Vector2(0, 0), 400, font_path, 35, tuple(Color("red")),
    [255, 255, 255, 0], "rtl",wholesome=True)

pillow_surface = text_box.text_surface
pillow_rect = pillow_surface.get_rect(top=screen.get_height() / 2, centerx=screen.get_width() / 2)

run = True
while run :
    screen.fill("gray")
    for i in pg.event.get() :
        if i.type == QUIT or i.type == KEYDOWN and i.key == K_ESCAPE :
            run = False

    screen.blit(pg_surface, pg_rect)
    screen.blit(pillow_surface, pillow_rect)

    pg.display.update()
