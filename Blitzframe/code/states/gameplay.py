from settings import *
from sprites import *
from tilemap import Tilemap
from support import *
from ui import *

class InGameStats:
    def __init__(self, game):
        self.game = game
        self.money = 0
        self.health = self.game.player.health
        self.wave = 1
        
        # upgrades
        self.health_upgrade = 1
        self.damage_upgrade = 1
        self.speed_upgrade = 1
        
    def update(self):
        self.health = self.game.player.health
        


class Gameplay:
    def __init__(self, game):
        
        self.game = game
        self.map = Tilemap(self.game.all_sprites, self.game.collision_sprites)

    def on_enter(self):
        if not hasattr(self.game, 'player'):
            self.game.player = Player((self.game.all_sprites), self.map.player_spawner(), self.game.collision_sprites, self.game.player_frames)
            self.game_stats = InGameStats(self.game)
            # self.wave_text_timer = Timer(1000, False, True, self.starting_wave)
            self.starting_wave()
            
               
    def input(self):
        keys = pygame.key.get_just_pressed()

        if keys[pygame.K_ESCAPE]:
            self.game.change_state('pause', False)
            
    def draw_game_ui(self):
        surface = pygame.display.get_surface()
        
        # ======== healthbar ========
        font = pygame.font.Font(None, 28)
        bar_width, bar_height = 200, 30
        x, y = 20, 20
        health = self.game_stats.health
        max_health = self.game.player.max_health if hasattr(self.game.player, 'max_health') else 100

        # задний фон
        pygame.draw.rect(surface, (60, 60, 60), (x, y, bar_width, bar_height), border_radius=8)
        # сколько хп
        fill_width = int(bar_width * (health / max_health))
        pygame.draw.rect(surface, (76, 184, 28), (x, y, fill_width, bar_height), border_radius=8)
        # обводка
        pygame.draw.rect(surface, (255, 255, 255), (x, y, bar_width, bar_height), 1, border_radius=8)

        # текст количества хп
        health_text = font.render(f'{health} / {max_health}', True, (255, 255, 255))
        text_rect = health_text.get_frect(center=(x + bar_width // 2, y + bar_height // 2))
        surface.blit(health_text, text_rect)

        # ======== player money ========
        font = pygame.font.Font(None, 40)
        x, y = 20, 70
        money_text = font.render(f'{self.game_stats.money} $', True, (0, 0, 0))
        text_rect = money_text.get_frect(topleft=(x, y))
        surface.blit(money_text, text_rect)


    def starting_wave(self):
        # draw wave number
        surface = pygame.display.get_surface()
        font = pygame.font.Font(None, 80)
        x, y = surface.width//2, 70
        self.fade_text = FadeText(f'Wave {self.game_stats.wave}', font, (82, 61, 80), (x, y))
        self.fade_text.start()


    def draw(self):
        self.game.all_sprites.draw(self.game.player.rect.center)
        self.draw_game_ui()
        self.fade_text.update(self.game.display_surface)

    def update(self, dt):
        self.input()
        self.game_stats.update()
        # self.wave_text_timer.update()


class InGameWindow:
    def __init__(self, game, title='', size=(400, 300)):
        self.game = game
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 50)
        self.bg_color = (30, 30, 30, 180)
        self.window_rect = pygame.Rect(0, 0, *size)
        self.window_rect.center = self.display_surface.get_rect().center
        self.title = title

    def on_enter(self):
        self.create_buttons()

    def draw(self):
        # игровой фон
        self.game.all_sprites.draw(self.game.player.rect.center)
        # затемнение
        overlay = pygame.Surface(self.display_surface.get_size(), pygame.SRCALPHA)
        overlay.fill(self.bg_color)
        self.display_surface.blit(overlay, (0, 0))
        # окно с закруглёнными краями
        window_surf = pygame.Surface(self.window_rect.size, pygame.SRCALPHA)
        window_surf.fill((0, 0, 0, 0)) 
        pygame.draw.rect(
            window_surf,
            (50, 50, 50, 220),
            window_surf.get_rect(),
            border_radius=20  
        )
        self.display_surface.blit(window_surf, self.window_rect.topleft)
        # заголовок
        if self.title:
            title_surf = self.font.render(self.title, True, 'white')
            title_rect = title_surf.get_rect(center=(self.window_rect.centerx, self.window_rect.top - 50))
            self.display_surface.blit(title_surf, title_rect)
            
        # кнопки
        self.game.buttons_sprites.draw(self.display_surface)

    def update(self, dt):
        self.game.buttons_sprites.update(dt)


class Pause(InGameWindow):
    def __init__(self, game, title='', size=(400, 300)):
        super().__init__(game, title, size)

    def on_enter(self):
        super().on_enter()
        self.game.game_paused = True

    def create_buttons(self):
        # resume
        self.resume_game_button = Button(
            groups=self.game.buttons_sprites,
            pos=(self.window_rect.x + self.window_rect.width//2, self.window_rect.y + self.window_rect.height//3),
            text='Resume',
            font=self.font,
            bg_color='#CA7842',
            text_color='#4B352A'
        )

    def input(self):
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_ESCAPE] or self.resume_game_button.is_clicked():
            self.game.change_state('gameplay', False)
            self.game.game_paused = False


    def update(self, dt):
        super().update(dt)
        self.input()
