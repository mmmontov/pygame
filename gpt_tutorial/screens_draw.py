from settings import *
from player import Player
from scope import Scope
from bullet import Bullet
from enemy import Enemy
from ui import *

def draw_game_screen(screen, bullets: list[Bullet], enemies: list[Enemy], scope: Scope, player: Player, ui: GameUi):
    screen.fill(COLORS['bg'])
    for bullet in bullets:
        bullet.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)

    player.draw(screen)
    scope.draw(screen)
    ui.draw_ui(screen)


# def draw_game_over_screen(screen, ui: GameOverUi):
#     screen.fill(COLORS['bg'])
#     buttons = ui.draw_ui(screen)
#     return buttons