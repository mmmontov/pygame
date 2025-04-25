import pygame
import sys
import time

from gun import Gun
from bullet import Bullet
from ino import Ino

def events(screen, gun: Gun, bullets):
    """обработка событий"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # движение вправо
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                gun.mright = True
            # движение влево
            if event.key == pygame.K_a:
                gun.mleft = True
            # стрельба                
            elif event.key == pygame.K_SPACE:
                new_bullet = Bullet(screen, gun)
                bullets.add(new_bullet)
            
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                gun.mright = False
        # движение влево
            if event.key == pygame.K_a:
                gun.mleft = False
    

def update(bg_color, screen, stats, score, gun, inos, bullets):
    """обновление экрана"""
    screen.fill(bg_color)
    score.show_score()

    for bullet in bullets.sprites():
        bullet.draw_bullet()
    gun.output()
    inos.draw(screen)
    pygame.display.flip()


def update_bullets(screen, inos, bullets, stats, score):
    """проверка позиции пули"""
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0: 
            bullets.remove(bullet)

    collisions = pygame.sprite.groupcollide(bullets, inos, True, True)
    if collisions:
        for values in collisions.values():
            stats.score += len(values)
        score.image_score()
        check_best_score(stats, score)
        score.image_guns()
    if len(inos) == 0:
        bullets.empty()
        create_army(screen, inos)


    # print(len(bullets))

def update_inos(stats, screen, gun, inos, bullets, score):
    """обновление позицию инопланетян"""
    inos.update()
    if pygame.sprite.spritecollideany(gun, inos):
        gun_kill(stats, screen, gun, inos, bullets, score)
    inos_check(stats, screen, gun, inos, bullets, score)

def create_army(screen, inos):
    """создание армии пришельцев"""
    ino = Ino(screen)
    ino_width = ino.rect.width
    ino_height = ino.rect.height
    number_ino_x = int((500 - 2*ino_width) / ino_width)
    number_ino_y = int((600 - 100 - 2*ino_height) / ino_height)
    
    for row in range(number_ino_y-2):
        for col in range(number_ino_x):
            ino = Ino(screen)
            ino.x = ino_width + ino_width * col
            ino.y = ino_height + ino_height * row
            ino.rect.x = ino.x
            ino.rect.y = ino.rect.height + ino.rect.height * row
            inos.add(ino)

def gun_kill(stats, screen, gun, inos, bullets, score):
    """столкновение пушки с пришельцами"""
    stats.guns_left -= 1
    if stats.guns_left > 0:
        score.image_guns()
        inos.empty()
        bullets.empty()

        create_army(screen, inos)
        gun.create_gun()
        time.sleep(1.5)

    else:
        stats.run_game = False

        with open('best_score.txt', 'w', encoding='utf-8') as file:
            file.write(str(stats.best_score))

        sys.exit()

def inos_check(stats, screen, gun, inos, bullets, score):
    """проверка пересечения пришельцами края экрана"""

    screen_rect = screen.get_rect()

    for ino in inos.sprites():
        if ino.rect.bottom >= screen_rect.bottom:
            gun_kill(stats, screen, gun, inos, bullets, score)
            break

def check_best_score(stats, score):
    """проверка нового рекорда"""

    if stats.score > stats.best_score:
        stats.best_score = stats.score
        score.image_best_score()