from settings import *
from support import *


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
        # print(self.frames, int(self.frame_index)%len(self.frames))
        self.image = self.frames[str(int(self.frame_index)%len(self.frames))]
        


class Player(AnimatedSprite):
    def __init__(self, groups, pos, collision_sprites, frames):
        super().__init__(groups, pos, frames) 
        self.state, self.frame_index = 'down', 0
        
        self.image = pygame.image.load('images/player/down/0.png').convert_alpha()
        self.rect = self.image.get_frect(center=pos)
        self.hitbox_rect = self.rect.inflate(-20, -40)
        
        # movement
        self.direction = pygame.Vector2()
        self.speed = 200
        
        # healthsssssss
        self.health = self.max_health = 100
        
        self.collision_sprites = collision_sprites
        
                             
    def input(self):
        keys = pygame.key.get_pressed()
        
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction
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
                    
    def animate(self, dt):
        # get state
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'
        if self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'
        
        
        # animate
        self.frame_index = self.frame_index + 10 * dt if self.direction else 0
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]
       
        
    def update(self, dt):  
        self.input()
        self.move(dt)
        # self.animate(dt)
        
        
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
        
        self.speed = random.randint(150, 180) * speed_multiplier
        print(speed_multiplier)
        

        
    
    
        
        
