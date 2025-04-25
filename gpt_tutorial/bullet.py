import pygame as pg
from settings import *

class Bullet:
    def __init__(self, pos: tuple[int], direction: pg.math.Vector2):
        self.pos = pg.math.Vector2(pos)
        self.direction = direction.normalize()
        self.speed = BULLET_SPEED
        self.color = COLORS['bullet']
        self.radius = BULLET_RADIUS

    def update(self):
        self.pos += self.direction*self.speed

    def draw(self, surface):
        pg.draw.circle(surface, self.color, self.pos, self.radius)


