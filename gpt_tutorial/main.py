import pygame as pg

from settings import *
from player import Player
from scope import Scope
from bullet import Bullet
from enemy import Enemy
from game_state import game_state
from ui import GameUi

from screens_draw import *

def main():
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pg.time.Clock()


    player = Player((SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    scope = Scope()

    bullets: list[Bullet] = []
    enemies: list[Enemy] = []

    enemy_timer = 0

    running = True
    while running:
        # === обработка событий ===
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                direction = pg.Vector2(pg.mouse.get_pos()) - player.rect.center
                bullets.append(Bullet(player.rect.center, direction))

        keys = pg.key.get_pressed()
        mouse = pg.mouse.get_pos()

        if game_state.current_screen == 'game':
            ui = GameUi()
            # === обновления ===
            for bullet in bullets:
                bullet.update()
                if bullet.pos.x > SCREEN_WIDTH or bullet.pos.x < 0 or bullet.pos.y < 0 or bullet.pos.y > SCREEN_HEIGHT:
                    bullets.remove(bullet)

            if enemy_timer > 100:
                enemies.append(Enemy())
                enemy_timer = 0
            enemy_timer += 1
            for enemy in enemies:
                alive = enemy.check_alive(bullets)
                if alive:
                    enemy.update(player.rect.center)
                else:
                    enemies.remove(enemy)

                if enemy.rect.colliderect(player.rect):
                    player.take_damage(enemy.damage)
                    enemy.deal_damage(player.rect.center)

            player.update(keys)
            scope.update(mouse)

            # === отрисовка ===
            draw_game_screen(screen, bullets, enemies, scope, player, ui)

        elif game_state.current_screen == 'game_over':
            ui = GameOverUi()
            # === обновления ===
            pass
            # === отрисовка ===
            draw_game_over_screen(screen, ui)
            


        pg.display.flip()
        clock.tick(FPS)

    pg.quit()


if __name__ == '__main__':
    main()
