import pygame
from random import randint, uniform


class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load('images/player.png').convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
        
        self.direction = pygame.math.Vector2()
        self.speed = 300

        # cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400

        
    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt):
        keys = pygame.key.get_pressed()
        recent_keys = pygame.key.get_just_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser((all_sprites, laser_sprites), laser_surf, self.rect.midtop)
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            laser_sound.play()

        self.laser_timer()

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)        
        self.image = surf
        cords = randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)
        self.rect = self.image.get_frect(center=cords)
      
class Laser(pygame.sprite.Sprite):
    def __init__(self, groups, surf, pos):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)

    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.original_surf = surf
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(self.image.width, WINDOW_WIDTH), -100)) 
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(400, 500)
        self.rotation_speed = randint(50, 100)
        self.rotation_angle = 0
    
    def update(self, dt):
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time == self.lifetime:
            self.kill()

        self.rect.center += self.direction * self.speed * dt

        self.rotation_angle += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation_angle, 1)
        self.rect = self.image.get_frect(center = self.rect.center)

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, groups, frames, pos):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = frames[self.frame_index]
        self.rect = self.image.get_frect(center=pos)

    def update(self, dt):
        self.frame_index += 20*dt 
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)%len(self.frames)]
        else: 
            self.kill()

def collisions():
    global running

    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, False, pygame.sprite.collide_mask)
    if collision_sprites:
        running = False

    for laser_sprite in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser_sprite, meteor_sprites, True)
        if collided_sprites:
            laser_sprite.kill()
            AnimatedExplosion(all_sprites, explosion_frames, laser_sprite.rect.midtop)
            explosion_sound.play()

def display_score():
    current_time = pygame.time.get_ticks() // 100
    text_surf = font.render(str(current_time), True, (240, 240, 240))
    text_rect = text_surf.get_frect(midbottom = (WINDOW_WIDTH//2, WINDOW_HEIGHT - 50))
    display_surface.blit(text_surf, text_rect)

    pygame.draw.rect(display_surface, (200, 200, 200), text_rect.inflate(30, 20).move(0, -7), width=5, border_radius=10)

# general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720 
clock = pygame.time.Clock()
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('space_shooter')
running = True

# imports
star_surf = pygame.image.load('images/star.png').convert_alpha()
laser_surf = pygame.image.load('images/laser.png').convert_alpha()
meteor_surf = pygame.image.load('images/meteor.png').convert_alpha()
font = pygame.font.Font('images/Oxanium-Bold.ttf', 40)
explosion_frames = [pygame.image.load(f'images/explosions/{i}.png').convert_alpha() for i in range(21)]

laser_sound = pygame.mixer.Sound('audio/laser.wav')
laser_sound.set_volume(0.02)
explosion_sound = pygame.mixer.Sound('audio/explosion.wav')
explosion_sound.set_volume(0.02)
game_music = pygame.mixer.Sound('audio/game_music.wav')
game_music.set_volume(0.01)
game_music.play(loops=-1)

# sprites
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

for _ in range(20):
    Star(all_sprites, star_surf)

player = Player(all_sprites)

# custom events
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

while running:
    dt = clock.tick()/1000
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            Meteor((all_sprites, meteor_sprites), meteor_surf)
        
    # update
    all_sprites.update(dt)
    collisions()

    # draw game
    display_surface.fill('#3a2e3f')
    all_sprites.draw(display_surface)
    display_score()

    pygame.display.update()

pygame.quit()