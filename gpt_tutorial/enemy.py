import pygame as pg
from random import choice, randint
from settings import *
from bullet import Bullet
from game_state import game_state

class Enemy(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.color = COLORS['enemy']
        self.speed = ENEMY_SPEED
        self.damage = 20
        self.worth = 1
        
        # рандомим координаты появления противника за границами экрана
        pos_x = randint(0, SCREEN_WIDTH)
        pos_y = randint(0, SCREEN_HEIGHT)

        moving_out_direction = choice([True, False])
        if moving_out_direction:
            pos_x += choice([SCREEN_WIDTH, -SCREEN_WIDTH])
        else:
            pos_y += choice([SCREEN_HEIGHT, -SCREEN_HEIGHT])

        self.rect = pg.Rect(0, 0, ENEMY_WIDTH, ENEMY_HEIGHT)
        self.rect.center = (pos_x, pos_y)

    def deal_damage(self, player_pos: tuple[int]):
        direction = pg.Vector2(player_pos) - self.rect.center
        self.rect.center -= direction.normalize() * 40

    def update(self, player_pos: tuple[int]):
        direction = pg.Vector2(player_pos) - self.rect.center
        # если входит ровно в игрока выскакивает ошибка деления на 0, починить
        self.rect.center += direction.normalize() * self.speed

    def draw(self, surface):
        pg.draw.rect(surface, self.color, self.rect, border_radius=10)

    def check_alive(self, bullets: list[Bullet]):
        for bullet in bullets:
            if self.rect.collidepoint(bullet.pos):
                bullets.remove(bullet)
                game_state.score += self.worth
                return False
        return True