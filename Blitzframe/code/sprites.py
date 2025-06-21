from settings import *
from support import *
from math import degrees, atan2, radians, cos, sin

class Sprite(pygame.sprite.Sprite):
    def __init__(self, groups, pos, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
        

class AnimatedSprite(Sprite):
    def __init__(self, groups, pos, frames):
        self.frames, self.frame_index, self.animation_speed = frames, 0, 5
        super().__init__(groups, pos, self.frames[str(self.frame_index)])
        
    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        frame = self.frames[str(int(self.frame_index) % len(self.frames))]
        
        if hasattr(self, "direction") and self.direction.x > 0:
                self.image = pygame.transform.flip(self.original_image, True, False)
        else:
            self.image = self.original_image
        
# =============== player =====================

class Player(Sprite):
    def __init__(self, groups, pos, collision_sprites, frames, game):
        # frames: dict[str, list[surf]]
        self.game = game
        self.all_sprites = groups
        self.frames = frames
        self.death_frame = pygame.image.load(join('images', 'player', 'death.png')).convert_alpha()
        self.death_frame = pygame.transform.scale(self.death_frame, (self.death_frame.get_width() * 3, self.death_frame.get_height() * 3))
        self.state = 'down'
        self.frame_index = 1
        self.last_state = 'down'
        super().__init__(groups, pos, self.frames[self.state][self.frame_index])
        self.rect = self.image.get_frect(center=pos)
        self.hitbox_rect = self.rect.inflate(-30, -50)

        # movement
        self.direction = pygame.Vector2()
        self.speed = 150
        self.knockback = True
        self.knockback_freeze_timer = None

        # health
        self.health = self.max_health = 100
        self.player_alive = True

        # colisions
        self.collision_sprites = collision_sprites

        # sounds 
        self.step_cooldown = False
        self.step_sounds = list(self.game.sound.step_sounds.values())
        def step_reset():
            self.step_cooldown = False
        self.step_timer = Timer(400, False, False, step_reset)

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        if self.direction.length_squared() > 0:
            self.direction = self.direction.normalize()
        
        if not self.step_cooldown and self.direction:
            random.choice(self.step_sounds).play()
            self.step_cooldown = True
            self.step_timer.activate()
        # ===== test ==============
        if keys[pygame.K_k]:
            self.health -= 3
        if keys[pygame.K_l]:
            self.health += 5
        # =========================

    def move(self, dt):
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center
        

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                self.knockback = False
                def knockback_on():
                    self.knockback = True
                self.knockback_freeze_timer = Timer(100, False, True, knockback_on)
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom

    def get_state(self):
        x, y = self.direction.x, self.direction.y
        if x == 0 and y == 0:
            return self.last_state
        if x > 0 and y < 0:
            return 'right_up'
        if x > 0 and y > 0:
            return 'right_down'
        if x < 0 and y < 0:
            return 'left_up'
        if x < 0 and y > 0:
            return 'left_down'
        if x > 0:
            return 'right'
        if x < 0:
            return 'left'
        if y > 0:
            return 'down'
        if y < 0:
            return 'up'
        return self.last_state

    def animate(self, dt):
        state = self.get_state()
        moving = self.direction.length_squared() > 0

        if moving:
            self.frame_index += 10 * dt
            self.last_state = state
        else:
            self.frame_index = 1
            state = self.last_state

        frame_list = self.frames[state]
        frame = frame_list[int(self.frame_index) % len(frame_list)]

        # Для левых направлений используем кадры из 'left', 'left_up', 'left_down', если они есть
        if state in ['left', 'left_up', 'left_down']:
            self.image = frame
        else:
            self.image = frame

        self.state = state

    def solid_move(self, dx, dy):
        '''плавное движение, чтобы сквозь объекты не кидало'''
        self.hitbox_rect.x += dx
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if dx > 0:
                    self.hitbox_rect.right = sprite.rect.left
                if dx < 0:
                    self.hitbox_rect.left = sprite.rect.right

        self.hitbox_rect.y += dy
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if dy > 0:
                    self.hitbox_rect.bottom = sprite.rect.top
                if dy < 0:
                    self.hitbox_rect.top = sprite.rect.bottom

        self.rect.center = self.hitbox_rect.center

    def death(self):
        self.player_alive = False
        self.image = self.death_frame

    def take_damage(self, enemy):
        if hasattr(self, 'knockback_timer') and self.knockback_timer and self.knockback_timer.active:
            return  
        
        self.health -= int(enemy.damage)
        
        
        self.game.play_sound('player_damage')
        
        
        # camera chake
        if self.health <= 20:
            self.all_sprites.shake(20)
        elif 20 < self.health <= 50:
            self.all_sprites.shake(15)
        elif 50 < self.health <= 80:
            self.all_sprites.shake(10)
        else:
            self.all_sprites.shake(5)
        
        # punch
        if self.knockback:
            direction = pygame.Vector2(self.rect.center) - pygame.Vector2(enemy.rect.center)
            if direction.length_squared() > 0:
                self.knockback_direction = direction.normalize()
                self.knockback_speed = 400 
                self.knockback_timer = Timer(100)
                self.knockback_timer.activate()
            else:
                self.knockback_direction = pygame.Vector2()
                self.knockback_timer = None
        self.knockback = False
        def knockback_on():
            self.knockback = True
        self.knockback_freeze_timer = Timer(500, False, True, knockback_on)


    def apply_knockback(self, dt):
        if hasattr(self, 'knockback_timer') and self.knockback_timer and self.knockback_timer.active:
            full_move = self.knockback_direction * self.knockback_speed * dt

            steps = int(full_move.length() // 2) + 1
            step = full_move / steps if steps > 0 else pygame.Vector2()

            for _ in range(steps):
                self.solid_move(step.x, step.y)

            self.knockback_timer.update()
        elif hasattr(self, 'knockback_timer') and self.knockback_timer:
            self.knockback_timer.deactivate()

                

    def update(self, dt):  
        if self.player_alive:
            self.input()
            self.move(dt)
            
            self.apply_knockback(dt)
            self.animate(dt)
            
            self.step_timer.update()
            if self.knockback_freeze_timer: self.knockback_freeze_timer.update()

# =============== enemies ====================
        
class Enemy(AnimatedSprite):
    def __init__(self, groups, pos, frames, player: Player, collision_sprites, health_multiplier=1, speed_multiplier=1, damage_multiplier=1):
        super().__init__(groups, pos, frames)
        self.death_timer = Timer(200, func=self.kill)
        self.player = player
        self.collision_active = True
        
        self.base_speed = self.speed = 100 * speed_multiplier
        self.base_damage = self.damage = 15 * damage_multiplier
        
        # timers
        def reset_speed():
            self.speed = self.base_speed
            self.damage = self.base_damage
        self.deal_damage_timer = Timer(1000, func=reset_speed)
        self.bump_timer = Timer(0)
        self.bump_dir_locked = False

    
        # rect
        self.hitbox_rect = self.rect.inflate(-20, -40)
        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2()
    
    def deal_damage(self):
        if not self.deal_damage_timer:
            self.damage = 0
            self.speed = 20
            self.deal_damage_timer.activate()
    
    def take_damage(self, damage):
        self.health -= damage
        # print(damage)
        if self.health <= 0:
            self.destroy()

    def destroy(self):
        self.collision_active = False
        self.player.game.play_sound('enemy_kill')
        self.death_timer.activate()
        self.animation_speed = 0
        self.image = pygame.mask.from_surface(self.image).to_surface()
        self.image.set_colorkey('black')
    

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.hitbox_rect.right = sprite.rect.left
                    elif self.direction.x < 0:
                        self.hitbox_rect.left = sprite.rect.right
                elif direction == 'vertical':
                    if self.direction.y > 0:
                        self.hitbox_rect.bottom = sprite.rect.top
                    elif self.direction.y < 0:
                        self.hitbox_rect.top = sprite.rect.bottom

                # временное обходное направление
                if not self.bump_timer:
                    offset = pygame.Vector2(self.player.rect.center) - pygame.Vector2(self.rect.center)

                    if direction == 'horizontal':
                        self.direction = pygame.Vector2(0, -1 if offset.y < 0 else 1)
                    else:
                        self.direction = pygame.Vector2(-1 if offset.x < 0 else 1, 0)

                    obstacle_size = max(sprite.rect.width, sprite.rect.height)
                    duration = int(obstacle_size * 11)
                    self.bump_timer = Timer(duration)
                    self.bump_timer.activate()



    
    def move(self, dt):
        if not self.bump_timer:
            player_pos = pygame.Vector2(self.player.rect.center) 
            enemy_pos = pygame.Vector2(self.rect.center)
            self.direction = (player_pos - enemy_pos).normalize()

        # Движение и столкновение
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')

        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')

        self.rect.center = self.hitbox_rect.center
        
    
    def draw_health(self, surface, offset):
        '''отрисовывается в groups.py'''
        bar_width = 40
        bar_height = 6

        health_ratio = max(self.health / self.max_health, 0)
        current_width = int(bar_width * health_ratio)

        x = self.rect.centerx + offset.x - bar_width // 2
        y = self.rect.top + offset.y - 12

        pygame.draw.rect(surface, (60, 60, 60), (x, y, bar_width, bar_height), border_radius=3)
        pygame.draw.rect(surface, (220, 30, 30), (x, y, current_width, bar_height), border_radius=3)
    
    def update(self, dt):
        self.death_timer.update()
        
        if not self.death_timer:
            if self.bump_timer:
                self.bump_timer.update()
                if not self.bump_timer:
                    self.bump_timer = None  # сброс ссылки после деактивации
            self.deal_damage_timer.update()
            self.move(dt)
            self.animate(dt)
        
    
class NormalEnemy(Enemy):
    def __init__(self, groups, pos, frames, player, collision_sprites, health_multiplier=1,  speed_multiplier=1, damage_multiplier=1):
        super().__init__(groups, pos, frames, player, collision_sprites, health_multiplier, speed_multiplier, damage_multiplier)  
        self.speed = random.randint(100, 120) * speed_multiplier
        self.max_health = self.health = 100 * health_multiplier
        self.base_damage = self.damage = 25 * damage_multiplier

class FastEnemy(Enemy):
    def __init__(self, groups, pos, frames, player, collision_sprites, health_multiplier=1,  speed_multiplier=1, damage_multiplier=1):
        super().__init__(groups, pos, frames, player, collision_sprites, health_multiplier,  speed_multiplier, damage_multiplier)
        self.speed = random.randint(150, 180) * speed_multiplier
        self.max_health = self.health = 50 * health_multiplier
        self.base_damage = self.damage = 15 * damage_multiplier
        
        
# ================== guns & bulet ====================


class Bullet(Sprite):
    def __init__(self, groups, pos, surf, direction: pygame.Vector2, damage: int = 100, lifetime: int = 2000, speed: int = 600):
        super().__init__(groups, pos, surf)
        self.direction = direction
        self.speed = speed
        self.lifetime_timer = Timer(lifetime, False, True, self.kill)   
        self.damage = damage

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        self.lifetime_timer.update()    


class Gun(pygame.sprite.Sprite):
    description = 'просто оружие'
    def __init__(self, groups, player: Player):
        self.all_sprites = groups
        self.player = player
        self.player_direction = pygame.Vector2(1, 0)
        
        # surfs
        self.gun_surf = self.load_surf()
        self.bullet_surf = pygame.image.load(join('images', 'guns', 'bullet.png')).convert_alpha()
        self.gun_surf = pygame.transform.smoothscale(
            self.gun_surf,
            (int(self.gun_surf.get_width() * 0.7), int(self.gun_surf.get_height() * 0.7))
        )
        self.gun_center = self.gun_surf.get_rect().center  
        super().__init__(groups)
        # self
        self.image = self.gun_surf
        self.rect = self.image.get_rect(center=(self.player.rect.center))
        self.offset = pygame.Vector2(13, 13)
        self.last_horizontal = 1
        
        self.base_damage = self.player.game.game_stats.damage_upgrade

    def get_direction(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        player_pos = pygame.Vector2(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
        self.player_direction = (mouse_pos - player_pos).normalize() if mouse_pos != player_pos else pygame.Vector2(1, 0)

    def update_side(self):
        if self.player.direction.x > 0:
            self.last_horizontal = 1
        elif self.player.direction.x < 0:
            self.last_horizontal = -1

    def get_offset_and_pivot(self):
        state = self.player.state
        if state == 'up' or state == 'right_up' or state == 'left_up':
            y_offset = -3
        else:
            y_offset = 15
        if state in ['right', 'right_up', 'right_down']:
            x_offset = 10
            pivot_offset = (-5, 0)
        elif state in ['left', 'left_up', 'left_down']:
            x_offset = -10
            pivot_offset = (5, 0)
        else:
            x_offset = 0
            pivot_offset = (0, 0)
        gun_dir_x = 1 if self.player_direction.x > 0 else -1
        if self.player.direction.x > 0:
            player_dir_x = 1
        elif self.player.direction.x < 0:
            player_dir_x = -1
        else:
            player_dir_x = self.last_horizontal
        if player_dir_x != gun_dir_x:
            x_offset = x_offset // 10
        return pygame.Vector2(x_offset, y_offset), pivot_offset

    def rotate_gun(self):
        angle = -degrees(atan2(self.player_direction.y, self.player_direction.x))
        flip = self.player_direction.x < 0
        gun_image = pygame.transform.flip(self.gun_surf, False, flip)
        offset, pivot_offset = self.get_offset_and_pivot()
        temp_surf = pygame.Surface(self.gun_surf.get_size(), pygame.SRCALPHA)
        temp_surf.blit(gun_image, (0, 0))
        rotated_image = pygame.transform.rotozoom(temp_surf, angle, 1)
        rotated_rect = rotated_image.get_rect(center=(self.player.rect.centerx + offset.x, self.player.rect.centery + offset.y))
        self.image = rotated_image
        self.rect = rotated_rect

    def create_bulet(self):
        pass # rewrite

    def input(self):
        mouse = pygame.mouse.get_pressed()
        if mouse[0]:
            self.create_bulet()

    def update(self, _):
        self.get_direction()
        self.update_side()
        self.rotate_gun()
        self.input()
        
        self.base_damage = self.player.game.game_stats.damage_upgrade


class Pistol(Gun):
    gun_name = 'pistol'    
    price = 0
    description = 'Пистолет - просто обычный пистолет,\nничего необычного'
    def __init__(self, groups, player):
        self.all_sprites, self.bullet_sprites = groups
        super().__init__(self.all_sprites, player)
        
        
        self.cooldown_timer = Timer(500)

    def load_surf(self):
        return pygame.image.load(join('images', 'guns', 'pistol.png')).convert_alpha()

    def create_bulet(self):
        if not self.cooldown_timer:
            self.player.game.play_sound('pistol_shot')
            Bullet((self.all_sprites, self.bullet_sprites), self.rect.center+self.player_direction*10, self.bullet_surf, self.player_direction, self.base_damage)
            self.cooldown_timer.activate()
    
    def update(self, dt):
        super().update(dt)
        self.cooldown_timer.update()


class Shotgun(Gun):
    gun_name = 'shotgun'
    description = 'Дробовик - хорошее оружие для\nближней дистанции.\nВыстреливает сразу много пуль,\nкоторые задевают нескольких противников.'
    price = 150
    def __init__(self, groups, player):
        self.all_sprites, self.bullet_sprites = groups
        super().__init__(self.all_sprites, player)
        
        self.bullets_count = 5
        self.damage = self.base_damage * 0.55
        
        self.cooldown_timer = Timer(1200)

    def load_surf(self):
        return pygame.image.load(join('images', 'guns', 'shotgun.png')).convert_alpha()

    def create_bulet(self):
        if not self.cooldown_timer:
            self.player.game.play_sound('shotgun_shot')
            self.player.game.play_sound('shotgun_reload')
            
            spread_angle = 35 
            base_angle = atan2(self.player_direction.y, self.player_direction.x)
            for _ in range(self.bullets_count):
                random_offset = random.uniform(-spread_angle/2, spread_angle/2)
                angle = base_angle + radians(random_offset)
                direction = pygame.Vector2(cos(angle), sin(angle))
                Bullet((self.all_sprites, self.bullet_sprites), self.rect.center+direction*10, self.bullet_surf, direction, self.damage, lifetime=300, speed=1000)
            self.cooldown_timer.activate()
    

    def update(self, dt):
        super().update(dt)
        self.cooldown_timer.update()
        if hasattr(self, 'reload_timer'):
            self.reload_timer.update()
        
        
class SniperRifle(Gun):
    gun_name = 'sniper'
    description = 'Снайперка - хороша для дальних дистанций\nможет прострелисть несколько противников,\nесли они стоят рядом.'
    price = 200
    def __init__(self, groups, player):
        self.all_sprites, self.bullet_sprites = groups
        super().__init__(self.all_sprites, player)
        
        self.damage = self.base_damage * 3
        self.cooldown_timer = Timer(1000)
        
    def load_surf(self):
        return pygame.image.load(join('images', 'guns', 'sniper.png')).convert_alpha()
    
    def create_bulet(self):
        if not self.cooldown_timer:
            self.player.game.play_sound('sniper_shot')
            self.reload_timer = Timer(400, False, True, lambda: self.player.game.play_sound('sniper_reload'))
            Bullet((self.all_sprites, self.bullet_sprites), self.rect.center+self.player_direction*10, self.bullet_surf, self.player_direction, self.damage, lifetime=2000, speed=3000)
            self.cooldown_timer.activate()
            
            
    def update(self, dt):
        super().update(dt)
        self.cooldown_timer.update()
        if hasattr(self, 'reload_timer'):
            self.reload_timer.update()
  
        
class MachineGun(Gun):
    gun_name = 'machine-gun'
    description = 'Автомат - скорострельное, удобное, крутое.\nНо маловато урона...'
    price = 100
    def __init__(self, groups, player):
        self.all_sprites, self.bullet_sprites = groups
        super().__init__(self.all_sprites, player)
        
        self.damage = self.base_damage * 0.35
        self.cooldown_timer = Timer(100)
        
    def load_surf(self):
        return pygame.image.load(join('images', 'guns', 'machine-gun.png')).convert_alpha()
    
    def create_bulet(self):
        if not self.cooldown_timer:
            self.player.game.play_sound('machine-gun_shot')
            Bullet((self.all_sprites, self.bullet_sprites), self.rect.center+self.player_direction*10, self.bullet_surf, self.player_direction, self.damage, lifetime=1000, speed=600)
            self.cooldown_timer.activate()
            
    def update(self, dt):
        super().update(dt)
        self.cooldown_timer.update()