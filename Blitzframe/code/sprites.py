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
        self.image = self.frames[str(int(self.frame_index)%len(self.frames))]
        
# =============== player =====================

class Player(Sprite):
    def __init__(self, groups, pos, collision_sprites, frames):
        # frames: dict[str, list[surf]]
        self.all_sprites = groups
        self.frames = frames
        self.state = 'down'
        self.frame_index = 1
        self.last_state = 'down'
        super().__init__(groups, pos, self.frames[self.state][self.frame_index])
        self.rect = self.image.get_frect(center=pos)
        self.hitbox_rect = self.rect.inflate(-30, -50)

        # movement
        self.direction = pygame.Vector2()
        self.speed = 150

        # health
        self.health = self.max_health = 100

        self.collision_sprites = collision_sprites

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        if self.direction.length_squared() > 0:
            self.direction = self.direction.normalize()
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

    def take_damage(self, enemy):
        self.health -= enemy.damage
        
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
        direction = pygame.Vector2(self.rect.center) - pygame.Vector2(enemy.rect.center)
        if direction.length_squared() > 0:
            self.knockback_direction = direction.normalize()
            self.knockback_speed = 400 
            self.knockback_timer = Timer(100)
            self.knockback_timer.activate()
        else:
            self.knockback_direction = pygame.Vector2()
            self.knockback_timer = None


    def apply_knockback(self, dt):
        if hasattr(self, 'knockback_timer') and self.knockback_timer and self.knockback_timer.active:
            move = self.knockback_direction * self.knockback_speed * dt
            self.hitbox_rect.x += move.x
            self.collision('horizontal')
            self.hitbox_rect.y += move.y
            self.collision('vertical')
            self.rect.center = self.hitbox_rect.center
            self.knockback_timer.update()
        elif hasattr(self, 'knockback_timer') and self.knockback_timer:
            self.knockback_timer.deactivate()

    def update(self, dt):  
        self.input()
        self.move(dt)
        self.apply_knockback(dt)
        self.animate(dt)

# =============== enemies ====================
        
class Enemy(AnimatedSprite):
    def __init__(self, groups, pos, frames, player, collision_sprites, speed_multiplier=1, damage_multiplier=1):
        super().__init__(groups, pos, frames)
        self.death_timer = Timer(200, func=self.kill)
        self.player = player
        self.base_speed = self.speed = 100 * speed_multiplier
        self.base_damage = self.damage = 15 * damage_multiplier
        self.max_health = self.health = 100
        
        # timers
        def reset_speed():
            self.speed = self.base_speed
            self.damage = self.base_damage
        self.deal_damage_timer = Timer(1000, func=reset_speed)

    
        # rect
        self.hitbox_rect = self.rect.inflate(-20, -40)
        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2()
    
    def deal_damage(self):
        self.damage = 0
        self.speed = 20
        self.deal_damage_timer.activate()
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.destroy()

    def destroy(self):
        self.death_timer.activate()
        self.animation_speed = 0
        self.image = pygame.mask.from_surface(self.image).to_surface()
        self.image.set_colorkey('black')
    
    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom
    
    def move(self, dt):
        # get direction
        player_pos = pygame.Vector2(self.player.rect.center) 
        enemy_pos = pygame.Vector2(self.rect.center)
        
        self.direction = (player_pos - enemy_pos).normalize()
        
        # udpate rect pos + collisions    
        self.hitbox_rect.x += self.direction.x * self.speed*dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed*dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center
    
    def draw_health(self):
        bar_width = 40
        bar_height = 6

        # Health ratio
        health_ratio = max(self.health / self.max_health, 0)
        current_width = int(bar_width * health_ratio)

        pygame.draw.rect(self.image, (60, 60, 60), (self.image.get_width()//2 - bar_width//2, 2, bar_width, bar_height), border_radius=10)
        pygame.draw.rect(self.image, (220, 30, 30), (self.image.get_width()//2 - bar_width//2, 2, current_width, bar_height), border_radius=10)

    
    def update(self, dt):
        self.death_timer.update()
        
        if not self.death_timer:
            self.deal_damage_timer.update()
            self.draw_health()
            self.move(dt)
            self.animate(dt)
        
    
class NormalEnemy(Enemy):
    def __init__(self, groups, pos, frames, player, collision_sprites, speed_multiplier=1, damage_multiplier=1):
        super().__init__(groups, pos, frames, player, collision_sprites, speed_multiplier, damage_multiplier)  
        print('normal')
        self.speed = random.randint(150, 180) * speed_multiplier
       

class FastEnemy(Enemy):
    def __init__(self, groups, pos, frames, player, collision_sprites, speed_multiplier=1, damage_multiplier=1):
        super().__init__(groups, pos, frames, player, collision_sprites, speed_multiplier, damage_multiplier)
        print('speed')
        self.speed = random.randint(200, 250) * speed_multiplier
        
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
    def __init__(self, groups, player: Player):
        self.all_sprites = groups
        self.player = player
        self.player_direction = pygame.Vector2(1, 0)
        self.gun_surf = self.load_surf()
        self.gun_surf = pygame.transform.smoothscale(
            self.gun_surf,
            (int(self.gun_surf.get_width() * 0.7), int(self.gun_surf.get_height() * 0.7))
        )
        self.gun_center = self.gun_surf.get_rect().center  
        super().__init__(groups)
        self.image = self.gun_surf
        self.rect = self.image.get_rect(center=(self.player.rect.center))
        self.offset = pygame.Vector2(13, 13)
        self.last_horizontal = 1
        
        self.damage = 50

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


class Pistol(Gun):
    gun_name = 'pistol'
    def __init__(self, groups, player):
        self.all_sprites, self.bullet_sprites = groups
        super().__init__(self.all_sprites, player)
        self.bullet_surf = pygame.image.load(join('images', 'guns', 'bullet.png')).convert_alpha()
        
        self.cooldown_timer = Timer(600)

    def load_surf(self):
        return pygame.image.load(join('images', 'guns', 'pistol.png')).convert_alpha()

    def create_bulet(self):
        if not self.cooldown_timer:
            Bullet((self.all_sprites, self.bullet_sprites), self.rect.center+self.player_direction*10, self.bullet_surf, self.player_direction, self.damage)
            self.cooldown_timer.activate()
    
    def update(self, dt):
        super().update(dt)
        self.cooldown_timer.update()


class Shotgun(Gun):
    gun_name = 'shotgun'
    def __init__(self, groups, player):
        self.all_sprites, self.bullet_sprites = groups
        super().__init__(self.all_sprites, player)
        self.bullet_surf = pygame.image.load(join('images', 'guns', 'bullet.png')).convert_alpha()
        self.bullets_count = 5
        self.damage *= 0.5
        
        self.cooldown_timer = Timer(1000)

    def load_surf(self):
        return pygame.image.load(join('images', 'guns', 'pistol.png')).convert_alpha()

    def create_bulet(self):
        if not self.cooldown_timer:
            spread_angle = 25  
            base_angle = atan2(self.player_direction.y, self.player_direction.x)
            for _ in range(self.bullets_count):
                random_offset = random.uniform(-spread_angle/2, spread_angle/2)
                angle = base_angle + radians(random_offset)
                direction = pygame.Vector2(cos(angle), sin(angle))
                Bullet((self.all_sprites, self.bullet_sprites), self.rect.center + direction * 10, self.bullet_surf, direction, self.damage, 300, 1000)
            self.cooldown_timer.activate()
    

    def update(self, dt):
        super().update(dt)
        self.cooldown_timer.update()