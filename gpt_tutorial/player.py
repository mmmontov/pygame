import pygame as pg
from settings import *
from game_state import game_state

class Player(pg.sprite.Sprite):
    def __init__(self, pos: tuple[int]):
        super().__init__()

        self.max_health = game_state.player_health
        self.speed = PLAYER_SPEED
        self.color = COLORS['player']
        self.rect = pg.Rect(0, 0, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.rect.center = pos

    def take_damage(self, damage):
        game_state.player_health -= damage
        
        if game_state.player_health <= 0:
            game_state.player_health = 0 
            self.die()

    def die(self):
        game_state.save_last_game_score()
        game_state.reset() 
        game_state.current_screen = 'game_over'  


    def update(self, keys_pressed):
        self.health = game_state.player_health
        if keys_pressed[pg.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys_pressed[pg.K_s] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed
        if keys_pressed[pg.K_d] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys_pressed[pg.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed

    def draw(self, surface):
        pg.draw.rect(surface, self.color, self.rect)

    