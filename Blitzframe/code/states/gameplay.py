from settings import *
from sprites import *
from tilemap import Tilemap
from support import *
from ui import *

from random import choice

class InGameStats:
    def __init__(self, game):
        self.game = game
        self.money = 0
        self.health = self.game.player.health
        self.wave = 1
        
        # wave
        self.prev_enemies_count = self.enemies_counter = 0
        self.wave_active = False
        
        # upgrades
        self.health_upgrade = 1
        self.damage_upgrade = 1
        self.speed_upgrade = 1
        
    def update(self):
        self.health = self.game.player.health
        self.prev_enemies_count = self.enemies_counter
        self.enemies_counter = len(self.game.enemy_sprites)
        if self.prev_enemies_count > self.enemies_counter:
            self.money += random.randint(50, 100)


class Gameplay:
    def __init__(self, game):
        self.game = game

    def on_enter(self):
        if not hasattr(self.game, 'player'):
            self.game.gameplay = self
            self.game.player = Player((self.game.all_sprites), self.game.tilemap.player_spawner(), self.game.collision_sprites, self.game.player_frames)
            self.game.current_gun = Shotgun((self.game.all_sprites, self.game.bullet_sprites), self.game.player)
            self.game_stats = InGameStats(self.game)
            self.game.game_stats = self.game_stats
            self.start_wave_timer()
               
    def start_wave_timer(self):
        self.starting_wave_timer = Timer(2000, False, True, self.starting_wave)
        
               
    def input(self):
        keys = pygame.key.get_just_pressed()

        if keys[pygame.K_ESCAPE]:
            self.game.change_state('pause', False)
        
        if keys[pygame.K_i]:
            for sprite in self.game.enemy_sprites:
                sprite.kill()
                break
        
            
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
        self.game_stats.wave_active = True
        # draw wave number
        surface = pygame.display.get_surface()
        font = pygame.font.Font(None, 80)
        x, y = surface.width//2, 70
        self.fade_text = FadeText(f'Wave {self.game_stats.wave}', font, (82, 61, 80), (x, y))
        self.fade_text.start()
        
        # starting wave
        wave_settings = load_json('settings/waves.json')[str(self.game_stats.wave)]
        enemies_dict = {
            'normal': NormalEnemy,
            'fast': FastEnemy
        }
        wave_multipliers = wave_settings['enemies_multiplier']
        
        # spawn enemies
        self.spawn_timers: list[Timer] = []
        for enemy_name, enemy_num in wave_settings['enemies'].items():
            for _ in range(enemy_num):
                
                self.spawn_timers.append(Timer(
                    random.randint(1000, 2000), 
                    False, 
                    True, 
                    lambda enemy_name = enemy_name: enemies_dict[enemy_name]((
                        self.game.all_sprites, self.game.enemy_sprites), 
                        choice(self.game.tilemap.enemy_spawner()),
                        self.game.enemies_frames_dict[enemy_name],
                        self.game.player,
                        self.game.collision_sprites,
                        speed_multiplier=wave_multipliers['speed'],
                        damage_multiplier=wave_multipliers['damage']
                        )))
        
    
    def ending_wave(self):
        self.game_stats.wave_active = False
        # draw wave congradulation
        surface = pygame.display.get_surface()
        font = pygame.font.Font(None, 80)
        x, y = surface.width//2, 70
        self.fade_text = FadeText(f'Wave {self.game_stats.wave} complete!', font, (82, 61, 80), (x, y))
        self.fade_text.start()
        
        # go to shop
        self.game_stats.wave += 1
        self.ending_wave_timer = Timer(2000, False, True, lambda: self.game.change_state('shop'))
                
    def collision(self):
        for bullet in self.game.bullet_sprites:
            sprite_collision = pygame.sprite.spritecollide(bullet, self.game.enemy_sprites, False, pygame.sprite.collide_mask)
            if sprite_collision:
                bullet.kill()
                for sprite in sprite_collision:
                    sprite.take_damage(bullet.damage)
        
        for enemy in self.game.enemy_sprites:
            if enemy.rect.colliderect(self.game.player.rect):
                self.game.player.take_damage(enemy)
                enemy.deal_damage()
        
           
    def draw(self):
        self.game.all_sprites.draw(self.game.player.rect.center)
        self.draw_game_ui()
        
        if hasattr(self, 'fade_text'):
            self.fade_text.update(self.game.display_surface)

        if hasattr(self, 'spawn_timers') and not self.spawn_timers and self.game_stats.enemies_counter == 0 and self.game_stats.wave_active:
            self.ending_wave()

            
    def update(self, dt):
        self.input()
        self.game_stats.update()
        self.collision()
        
        # timers
        self.starting_wave_timer.update()
        
        if hasattr(self, 'ending_wave_timer'):
            self.ending_wave_timer.update()
        
        if hasattr(self, 'spawn_timers'):
            for timer in self.spawn_timers:
                timer.update()
                if not timer: 
                    self.spawn_timers.remove(timer)
                    
        
        


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
        self.menu_button = Button(
            groups=self.game.buttons_sprites,
            pos=(self.window_rect.x + self.window_rect.width//2, self.window_rect.y + self.window_rect.height//3 + 100),
            text='Menu',
            font=self.font,
            bg_color='#CA7842',
            text_color='#4B352A'
        )

    def input(self):
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_ESCAPE] or self.resume_game_button.is_clicked():
            self.game.change_state('gameplay', False)
            self.game.game_paused = False

        if self.menu_button.is_clicked():
            self.game.change_state('main_menu')
            self.game.reset_game()

    def update(self, dt):
        super().update(dt)
        self.input()


class Shop(InGameWindow):
    def __init__(self, game, title='Shop', size=(800, 520)):  # уменьшили высоту окна
        super().__init__(game, title, size)

    def on_enter(self):
        super().on_enter()
        self.game.game_paused = True

    def create_buttons(self):
        # 3 столбца и 2 строки, увеличенные кнопки и большие отступы
        self.buttons = []
        cols = 3
        rows = 2
        horizontal_margin = 80   # большой отступ от левого и правого края окна
        vertical_margin_top = 120  # большой отступ сверху от заголовка
        vertical_margin_bottom = 80  # большой отступ снизу
        button_spacing_x = 60   # большое расстояние между столбцами
        button_spacing_y = 60   # большое расстояние между строками

        # вычисляем размеры кнопок
        available_width = self.window_rect.width - 2 * horizontal_margin - (cols - 1) * button_spacing_x
        button_width = available_width // cols
        available_height = self.window_rect.height - vertical_margin_top - vertical_margin_bottom - (rows - 1) * button_spacing_y
        button_height = available_height // rows

        for col in range(cols):
            for row in range(rows):
                x = self.window_rect.left + horizontal_margin + col * (button_width + button_spacing_x) + button_width // 2
                y = self.window_rect.top + vertical_margin_top + row * (button_height + button_spacing_y) + button_height // 2
                if col == 1 and row == 0:
                    btn = Button(
                        groups=self.game.buttons_sprites,
                        pos=(x, y),
                        text=f'Start wave',
                        font=self.font,
                        bg_color='#CA7842',
                        text_color='#4B352A',
                        size=(button_width, button_height),
                        callback='next_wave'
                    )

                    self.buttons.append(btn)
    
    def input(self):
        for btn in self.buttons:
            if btn.is_clicked() and btn.callback == 'next_wave':
                self.game.change_state('gameplay')
                self.game.game_paused = False
                self.game.gameplay.start_wave_timer()
                
    def update(self, dt):
        super().update(dt)
        self.input()