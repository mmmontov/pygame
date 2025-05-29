from settings import *
from support import *
from math import degrees, atan2

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
        self.frames = frames
        self.state = 'down'
        self.frame_index = 1
        self.last_state = 'down'
        super().__init__(groups, pos, self.frames[self.state][self.frame_index])
        self.rect = self.image.get_frect(center=pos)
        self.hitbox_rect = self.rect.inflate(-30, -50)

        # movement
        self.direction = pygame.Vector2()
        self.speed = 200

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

    def update(self, dt):  
        self.input()
        self.move(dt)
        self.animate(dt)
# =============== enemies ====================
        
class Enemy(AnimatedSprite):
    def __init__(self, groups, pos, frames, player, collision_sprites, speed_multiplier=1, damage_multiplier=1):
        super().__init__(groups, pos, frames)
        self.death_timer = Timer(200, func=self.kill)
        self.player = player
        self.speed = 100 * speed_multiplier
        self.damage = 15 * damage_multiplier
    
        # rect
        self.hitbox_rect = self.rect.inflate(-20, -40)
        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2()
    

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
    
    def update(self, dt):
        self.death_timer.update()
        if not self.death_timer:
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
        
# ================== guns ====================

class Gun(pygame.sprite.Sprite):
    def __init__(self, groups, player: Player):
        self.player = player
        self.player_direction = pygame.Vector2(1, 0)
        self.gun_surf = self.load_surf()
        # Масштабируем модельку оружия (например, 0.7x)
        self.gun_surf = pygame.transform.smoothscale(
            self.gun_surf,
            (int(self.gun_surf.get_width() * 0.7), int(self.gun_surf.get_height() * 0.7))
        )
        self.gun_center = self.gun_surf.get_rect().center  # Save original center

        super().__init__(groups)
        self.image = self.gun_surf
        self.rect = self.image.get_rect(center=(self.player.rect.center))

        # Смещение оружия (по умолчанию вправо)
        self.offset = pygame.Vector2(13, 13)
        # Сохраняем последнюю горизонтальную сторону (1 - вправо, -1 - влево)
        self.last_horizontal = 1

    def get_direction(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        player_pos = pygame.Vector2(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
        self.player_direction = (mouse_pos - player_pos).normalize() if mouse_pos != player_pos else pygame.Vector2(1, 0)

    def update_side(self):
        # Если игрок двигается по горизонтали, обновляем сторону
        if self.player.direction.x > 0:
            self.last_horizontal = 1
        elif self.player.direction.x < 0:
            self.last_horizontal = -1
        # Если игрок не двигается, сторона не меняется

    def get_offset_and_pivot(self):
        # Определяем смещение и точку вращения в зависимости от направления
        state = self.player.state
        # Смещение по вертикали: если вверх — выше центра, иначе ниже
        if state == 'up' or state == 'right_up' or state == 'left_up':
            y_offset = -3
        else:
            y_offset = 15

        # Смещение по горизонтали: если вправо — немного левее центра, если влево — немного правее
        if state in ['right', 'right_up', 'right_down']:
            x_offset = 10
            pivot_offset = (-5, 0)  # Вращаем чуть левее центра
        elif state in ['left', 'left_up', 'left_down']:
            x_offset = -10
            pivot_offset = (5, 0)   # Вращаем чуть правее центра
        else:
            x_offset = 0
            pivot_offset = (0, 0)

        # --- Смещение к центру, если направление движения игрока (лево/право) отличается от направления оружия ---
        # Определяем направление взгляда оружия (по горизонтали)
        gun_dir_x = 1 if self.player_direction.x > 0 else -1
        player_dir_x = 1 if self.player.direction.x > 0 else -1 if self.player.direction.x < 0 else gun_dir_x

        if player_dir_x != gun_dir_x:
            # Смещаем к центру игрока (например, на 10 пикселей)
            x_offset = x_offset // 10

        return pygame.Vector2(x_offset, y_offset), pivot_offset

    def rotate_gun(self):
        angle = -degrees(atan2(self.player_direction.y, self.player_direction.x))
        flip = self.player_direction.x < 0

        # Зеркалируем спрайт если нужно
        gun_image = pygame.transform.flip(self.gun_surf, False, flip)

        # Получаем смещение и смещение центра вращения
        offset, pivot_offset = self.get_offset_and_pivot()

        # Центр вращения: немного левее/правее центра изображения
        pivot = (self.gun_surf.get_width() // 2 + pivot_offset[0],
                 self.gun_surf.get_height() // 2 + pivot_offset[1])

        # Вращаем вокруг pivot (смещаем изображение так, чтобы pivot стал центром, потом вращаем)
        temp_surf = pygame.Surface(self.gun_surf.get_size(), pygame.SRCALPHA)
        temp_surf.blit(gun_image, (0, 0))
        rotated_image = pygame.transform.rotozoom(temp_surf, angle, 1)

        # Новый rect с pivot в центре
        rotated_rect = rotated_image.get_rect(center=(self.player.rect.centerx + offset.x, self.player.rect.centery + offset.y))

        self.image = rotated_image
        self.rect = rotated_rect

    def update(self, _):
        self.get_direction()
        self.update_side()
        self.rotate_gun()
             
class Pistol(Gun):
    def __init__(self, groups, player):
        super().__init__(groups, player)
        
    def load_surf(self):
        return pygame.image.load(join('images', 'guns', 'pistol.png')).convert_alpha()