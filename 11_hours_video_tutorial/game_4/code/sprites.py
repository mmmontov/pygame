from settings import *
from support import *
from math import sin
from random import randint, choice

class Sprite(pygame.sprite.Sprite):
    def __init__(self, groups, pos, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
        # self.ground = True


class Bullet(Sprite):
    def __init__(self, groups, pos, surf, direction):
        super().__init__(groups, pos, surf)
        
        # movement
        self.direction = direction
        self.speed = 850
        
        # adjusment 
        self.image = pygame.transform.flip(self.image, direction == -1, 0)
    
    def update(self, dt):
        self.rect.x += self.direction * self.speed * dt


class AnimatedSprite(Sprite):
    def __init__(self, groups, pos, frames):
        self.frames, self.frame_index, self.animation_speed = frames, 0, 10
        super().__init__(groups, pos, self.frames[self.frame_index])
        
    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index)%len(self.frames)]


class Player(AnimatedSprite):
    def __init__(self, groups, pos, collision_sprites, frames, create_bullet):
        super().__init__(groups, pos, frames)

        self.create_bullet = create_bullet

        # move 
        self.collision_sprites = collision_sprites
        self.flip = False
        self.direction = pygame.Vector2()
        self.speed = 500
        self.gravity = 20
        self.on_floor = False

        # timer
        self.shoot_timer = Timer(400)
        
    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.rect.right = sprite.rect.left
                    if self.direction.x < 0: self.rect.left = sprite.rect.right
                else:
                    if self.direction.y > 0: self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0: self.rect.top = sprite.rect.bottom
                    self.direction.y = 0
        
    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        
        
        just_keys = pygame.key.get_just_pressed()
        if just_keys[pygame.K_SPACE] and self.on_floor:
            self.direction.y -= 5
            
        if keys[pygame.K_LSHIFT] and not self.shoot_timer:
            self.create_bullet(self.rect.center, -1 if self.flip else 1)
            self.shoot_timer.activate()

    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        
        self.direction.y += self.gravity * dt
        self.rect.y += self.direction.y
        self.collision('vertical')
        
    def check_floor(self):
        bottom_rect = pygame.FRect((0, 0), (self.rect.width, 2)).move_to(midtop=self.rect.midbottom)
        level_rects = [sprite.rect for sprite in self.collision_sprites]
        self.on_floor = True if bottom_rect.collidelist(level_rects) >= 0 else False
    
    def animate(self, dt):
        if self.direction.x:
            self.frame_index += self.animation_speed * dt
            self.flip = self.direction.x < 0
        else:
            self.frame_index = 0
            
        
        self.frame_index = 1 if not self.on_floor else self.frame_index 
            
        self.image = self.frames[int(self.frame_index)%len(self.frames)]
        self.image = pygame.transform.flip(self.image, self.flip, False)
    
    def update(self, dt):
        self.shoot_timer.update()
        self.check_floor()
        self.input()
        self.move(dt)
        self.animate(dt)

       
class Fire(Sprite):
    def __init__(self, groups, pos, surf, player: Player):
        super().__init__(groups, pos, surf)
        self.player = player
        self.flip = player.flip
        self.timer = Timer(100, autostart=True, func=self.kill)
        self.y_offset = pygame.Vector2(0, 8)
        
        
        if self.player.flip:
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect.midright = self.player.rect.midleft + self.y_offset
        else:
            self.rect.midleft = self.player.rect.midright + self.y_offset
        
    def update(self, dt):
        
        if self.player.flip:
            self.rect.midright = self.player.rect.midleft + self.y_offset
        else:
            self.rect.midleft = self.player.rect.midright + self.y_offset
            
        if self.flip != self.player.flip:
            self.kill()
        
        self.timer.update()
        
     
class Enemy(AnimatedSprite):
    def __init__(self, groups, pos, frames):
        super().__init__(groups, pos, frames)
        self.death_timer = Timer(200, func=self.kill)
        
     
    def destroy(self):
        self.death_timer.activate()
        self.animation_speed = 0
        self.image = pygame.mask.from_surface(self.image).to_surface()
        self.image.set_colorkey('black')
     
    def update(self, dt):
        self.death_timer.update()
        if not self.death_timer:
            self.move(dt)
            self.animate(dt)
        self.constraint()


class Bee(Enemy):
    def __init__(self, groups, pos, frames):
        super().__init__(groups, pos, frames)
        self.speed = randint(300, 500)
        self.amplitude = randint(500, 600)
        self.frequency = randint(300, 600)
    
    def move(self, dt):
        self.rect.x -= self.speed * dt
        self.rect.y += sin(pygame.time.get_ticks()  / self.frequency) * self.amplitude * dt
        
    def constraint(self):
        if self.rect.right <= 0:
            self.kill()
            
        
class Worm(Enemy):
    def __init__(self, groups, rect, frames):
        super().__init__(groups, rect.topleft, frames)

        self.rect.bottomleft = rect.bottomleft 
        self.main_rect = rect
        
        self.direction = 1
        self.speed = randint(100, 200)
        
    def move(self, dt):
        self.rect.x += self.direction * self.speed * dt

        
    def constraint(self):
        if not self.main_rect.contains(self.rect):
            self.direction *= -1
            self.frames = [pygame.transform.flip(surf, True, False) for surf in self.frames]
        
    
