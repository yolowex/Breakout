import pygame as pg
from pygame.math import Vector2 as Pos
from pygame.rect import Rect

percent = lambda All,part: (100/All) * part

import math

"""
function RectCircleColliding(circle,rect){
    var distX = Math.abs(circle.x - rect.x-rect.w/2);
    var distY = Math.abs(circle.y - rect.y-rect.h/2);

    if (distX > (rect.w/2 + circle.r)) { return false; }
    if (distY > (rect.h/2 + circle.r)) { return false; }

    if (distX <= (rect.w/2)) { return true; } 
    if (distY <= (rect.h/2)) { return true; }

    var dx=distX-rect.w/2;
    var dy=distY-rect.h/2;
    return (dx*dx+dy*dy<=(circle.r*circle.r));
}
"""

def polygon( surface, color, center: Pos, radius, edges, angle=0,width=0 ) :
    top = center.copy()
    top.y -= radius

    points = [rotate(center, top, ((360 / edges) * j + angle)) for j in range(edges)]

    return pg.draw.polygon(surface, color, points,width=width)

def cap(num,min_,max_):
    if num < min_: num = min_
    if num > max_: num = max_
    return num

def rotate(origin, point, angle):
    angle = math.radians(angle)
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy


def RectCircleCollision(circle_center:Pos,circle_radius,rect:Rect):
    distX = abs(circle_center.x - rect.x-rect.w/2)
    distY = abs(circle_center.y - rect.y-rect.h/2)

    if distX > (rect.w/2 + circle_radius): return False
    if distY > (rect.h/2 + circle_radius): return False

    dx = distX - rect.w/2
    dy = distY - rect.h/2

    return dx*dx+dy*dy<=(circle_radius*circle_radius)
