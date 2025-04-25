import pygame as pg

from controls import events
from core.camera import Camera
from core.map import GameMap
from entities.player import Player

def run():
    pg.init()
    screen_width, screen_height = 960, 540

    screen = pg.display.set_mode((screen_width, screen_height))
    clock = pg.time.Clock()
    game_map = GameMap('assets/game_map.jpg')
    player = Player((game_map.image.get_width()//2,
                     game_map.image.get_height()//2))
    camera = Camera((screen_width, screen_height), 
                    (game_map.image.get_width(), 
                    game_map.image.get_height()))

    all_sprites = pg.sprite.Group(player)

    while True:
        events()
        player.update()
        camera.update(player.rect)


        screen.fill((30, 30, 30))  # фон
        game_map.draw(screen, camera.camera_rect)

        for sprite in all_sprites:
            screen.blit(sprite.image, camera.move_object(sprite.rect))
    
        pg.display.flip()
        clock.tick(60)


run()
