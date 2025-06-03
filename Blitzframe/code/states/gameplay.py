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
        self.health_upgrade = 100
        self.damage_upgrade = 50
        self.speed_upgrade = 150
        
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
            self.game.current_gun = Pistol((self.game.all_sprites, self.game.bullet_sprites), self.game.player)
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
                
        if keys[pygame.K_q]:
            self.game.available_weapons[Shotgun.gun_name] = Shotgun
            print('shot added')
            print(self.game.available_weapons)
        if keys[pygame.K_1]:
            self.game.change_gun(Pistol.gun_name)
            print(Pistol.gun_name)
        if keys[pygame.K_2]:
            self.game.change_gun(Shotgun.gun_name)
            print(Shotgun.gun_name)

            
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
        self.width, self.height = size
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
    def __init__(self, game, title='Shop', size=(800, 520)):
        super().__init__(game, title, size)

    def on_enter(self):
        super().on_enter()
        self.game.game_paused = True

    def create_buttons(self):
        cols = 3
        rows = 4
        horizontal_margin = 40
        vertical_margin_top = 100
        vertical_margin_bottom = 80
        button_spacing_x = 20
        button_spacing_y = 20

        # размеры кнопок
        available_width = self.window_rect.width - 2 * horizontal_margin - (cols - 1) * button_spacing_x
        button_width = available_width // cols
        available_height = self.window_rect.height - vertical_margin_top - vertical_margin_bottom - (rows - 1) * button_spacing_y
        button_height = available_height // rows

        # матрица кнопок
        self.buttons = [[None for _ in range(cols)] for _ in range(rows)]

        for row in range(rows):
            for col in range(cols):
                x = self.window_rect.left + horizontal_margin + col * (button_width + button_spacing_x) + button_width // 2
                y = self.window_rect.top + vertical_margin_top + row * (button_height + button_spacing_y) + button_height // 2
                btn = None

                # Start wave
                if row == 0 and col == 1:
                    btn = Button(
                        groups=self.game.buttons_sprites,
                        pos=(x, y),
                        text='Start wave',
                        font=self.font,
                        bg_color='#CA7842',
                        text_color='#4B352A',
                        size=(button_width, button_height),
                        callback='next_wave'
                    )
                
                # ====== upgrades ======
                # health upgrade
                if row == 1 and col == 2:
                    btn = Button(
                        groups=self.game.buttons_sprites,
                        pos=(x, y),
                        text=f'health +',
                        font=self.font,
                        bg_color='#CA7842',
                        text_color='#4B352A',
                        size=(button_width, button_height),
                        callback='health_upgrade'  
                    )
                # damage upgrade
                if row == 2 and col == 2:
                    btn = Button(
                        groups=self.game.buttons_sprites,
                        pos=(x, y),
                        text=f'damage +',
                        font=self.font,
                        bg_color='#CA7842',
                        text_color='#4B352A',
                        size=(button_width, button_height),
                        callback='damage_upgrade'  
                    )
                # speed upgrade
                if row == 3 and col == 2:
                    btn = Button(
                        groups=self.game.buttons_sprites,
                        pos=(x, y),
                        text=f'speed +',
                        font=self.font,
                        bg_color='#CA7842',
                        text_color='#4B352A',
                        size=(button_width, button_height),
                        callback='speed_upgrade'  
                    )
                
                # ====== guns ======
                # pistol
                if row == 0 and col == 0:
                    gun_name = Pistol.gun_name
                    if Pistol.gun_name in self.game.available_weapons:
                        btn = Button(
                            groups=self.game.buttons_sprites,
                            pos=(x, y),
                            text=gun_name,
                            font=self.font,
                            bg_color='#CA7842',
                            text_color='#4B352A',
                            size=(button_width, button_height),
                            callback=f'select_{gun_name}' 
                        )
                    else:
                        btn = Button(
                            groups=self.game.buttons_sprites,
                            pos=(x, y),
                            text=f'buy: {gun_name}',
                            font=self.font,
                            bg_color='#CA7842',
                            text_color='#4B352A',
                            size=(button_width, button_height),
                            callback=f'buy_{gun_name}' 
                        )
                
                # shotgun
                if row == 1 and col == 0:
                    gun_name = Shotgun.gun_name
                    if Shotgun.gun_name in self.game.available_weapons:
                        btn = Button(
                            groups=self.game.buttons_sprites,
                            pos=(x, y),
                            text=gun_name,
                            font=self.font,
                            bg_color='#CA7842',
                            text_color='#4B352A',
                            size=(button_width, button_height),
                            callback=f'select_{gun_name}' 
                        )
                    else:
                        btn = Button(
                            groups=self.game.buttons_sprites,
                            pos=(x, y),
                            text=f'buy: {gun_name}',
                            font=self.font,
                            bg_color='#CA7842',
                            text_color='#4B352A',
                            size=(button_width, button_height),
                            callback=f'buy_{gun_name}' 
                        )
                
                
                if btn: self.buttons[row][col] = btn

    def input(self):
        for row in self.buttons:
            for btn in row:
                btn: Button
                if btn and btn.is_clicked():
                    # ====== upgrades ======
                    if btn.callback == 'next_wave':
                        self.game.change_state('gameplay')
                        self.game.game_paused = False
                        self.game.gameplay.start_wave_timer()
                        
                    if btn.callback == 'health_upgrade':
                        self.game.game_stats.health_upgrade += 20
                        self.game.player.max_health = self.game.game_stats.health_upgrade
                    
                    if btn.callback == 'damage_upgrade':
                        self.game.game_stats.damage_upgrade += 5
                        self.game.current_gun.damage = self.game.game_stats.damage_upgrade
                    
                    if btn.callback == 'speed_upgrade':
                        self.game.game_stats.speed_upgrade += 10
                        self.game.player.speed = self.game.game_stats.speed_upgrade

                    # ====== guns ======
                    pistol = Pistol.gun_name
                    if btn.callback == f'select_{pistol}':
                        self.game.change_gun(pistol)
                    if btn.callback == f'buy_{pistol}':
                        btn.text = pistol
                        btn.callback = f'select_{pistol}'
                        self.game.available_weapons[pistol] = Pistol

                    shotgun = Shotgun.gun_name
                    if btn.callback == f'select_{shotgun}':
                        self.game.change_gun(shotgun)
                    if btn.callback == f'buy_{shotgun}':
                        btn.text = shotgun
                        btn.callback = f'select_{shotgun}'
                        self.game.available_weapons[shotgun] = Shotgun


    def draw_stats(self):
        font = pygame.font.Font(None, 36)
        color = (255, 255, 255)

        col = 1
        start_row = 0
        line_spacing = 40

        base_btn = self.buttons[start_row][col]
        if base_btn:
            base_x = base_btn.rect.centerx
            base_y = base_btn.rect.bottom + line_spacing 
        else:
            base_btn = self.window_rect
            base_x = base_btn.center
            base_y = base_btn.center

        # Health upgrade
        health_text = font.render(f"Health: {(self.game.game_stats.health_upgrade - 100) // 20 + 1}", True, color)
        health_rect = health_text.get_rect(center=(base_x, base_y))
        self.display_surface.blit(health_text, health_rect)

        # Damage upgrade
        damage_text = font.render(f"Damage: {(self.game.game_stats.damage_upgrade - 50) // 5 + 1}", True, color)
        damage_rect = damage_text.get_rect(center=(base_x, base_y + line_spacing))
        self.display_surface.blit(damage_text, damage_rect)

        # Speed upgrade
        speed_text = font.render(f"Speed: {(self.game.game_stats.speed_upgrade - 150) // 10 + 1}", True, color)
        speed_rect = speed_text.get_rect(center=(base_x, base_y + 2 * line_spacing))
        self.display_surface.blit(speed_text, speed_rect)

        # current gun
        current_gun = font.render(f'gun: {self.game.current_gun.gun_name}', True, color)
        current_gun_rect = current_gun.get_rect(center=(base_x, base_y + 4 * line_spacing))
        self.display_surface.blit(current_gun, current_gun_rect)

    def draw(self):
        super().draw()
        self.draw_stats()
        

    def update(self, dt):
        super().update(dt)
        self.input()