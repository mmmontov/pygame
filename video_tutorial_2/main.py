import pygame 
from pygame.sprite import Group

from gun import Gun
import controls
from stats import Stats
from score import Score


def run(): 
    pygame.init()
    screen = pygame.display.set_mode((500, 600))
    caption = pygame.display.set_caption('Space')

    bg_color = (0, 0, 0)

    gun = Gun(screen)
    bullets = Group()

    inos = Group()
    controls.create_army(screen, inos)

    stats = Stats()
    stats.reset_stats()

    score = Score(screen, stats)

    while True:
        controls.events(screen, gun, bullets)
        if stats.run_game:
            gun.update_gun()
            bullets.update()
            controls.update(bg_color, screen, stats, score, gun, inos, bullets)
            controls.update_bullets(screen, inos, bullets, stats, score)
            controls.update_inos(stats, screen, gun, inos, bullets, score)
        


run()