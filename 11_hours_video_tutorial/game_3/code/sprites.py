from settings import *
from random import choice, uniform


class Paddle(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        
        self.image = pygame.Surface(SIZE['paddle'], pygame.SRCALPHA)
        pygame.draw.rect(self.image, COLORS['paddle'], pygame.FRect((0, 0), SIZE['paddle']), 0, 5)
        self.rect = self.image.get_frect()
        
        # shadow
        self.shadow_surf = self.image.copy()
        pygame.draw.rect(self.shadow_surf, COLORS['paddle shadow'], pygame.FRect((0, 0), SIZE['paddle']), 0, 5)
        
                
        # move
        self.direction = pygame.Vector2()
        

    def move(self, dt):
        self.rect.center += self.direction * self.speed * dt
        
        self.rect.top = 0 if self.rect.top < 0 else self.rect.top
        self.rect.bottom = WINDOW_HEIGHT if self.rect.bottom > WINDOW_HEIGHT else self.rect.bottom

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.move(dt)


class Player(Paddle):
    def __init__(self, groups):
        super().__init__(groups)
        self.rect.center = POS['player']
        self.old_rect = self.rect.copy()
        self.speed = SPEED['player'] 
        
        
    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction
        
        
class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, paddle_sprites: list[Player], update_score):
        super().__init__(groups)
        self.paddle_sprites = paddle_sprites
        self.update_score = update_score
        
        # image
        self.image = pygame.Surface(SIZE['ball'], pygame.SRCALPHA)
        pygame.draw.circle(self.image, COLORS['ball'], (SIZE['ball'][0]/2, SIZE['ball'][1]/2), radius=SIZE['ball'][0]/2)
        # self.image.fill(COLORS['ball'])
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        
        # shadow
        self.shadow_surf = self.image.copy()
        pygame.draw.circle(self.shadow_surf, COLORS['ball shadow'], (SIZE['ball'][0]/2, SIZE['ball'][1]/2), radius=SIZE['ball'][0]/2)
        
        
        # movement
        self.direction = pygame.Vector2(choice((1, -1)), uniform(0.7, 0.8)*choice((1, -1)))
        self.old_rect = self.rect.copy()
        self.speed = SPEED['ball']
        
        # time
        self.reset_delay = 1000
        self.reset_time = 0
        
    def move(self, dt):
        if pygame.time.get_ticks() - self.reset_time > 1000:
            self.rect.x += self.direction.x * self.speed * dt
            self.collision('horizontal')
            self.rect.y += self.direction.y * self.speed * dt
            self.collision('vertical')
        
        
    def collision(self, direction):
        for sprite in self.paddle_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                        self.direction.x *= -1
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                        self.direction.x *= -1
                else:
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.direction.y *= -1
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        self.direction.y *= -1
         
    def wall_collision(self): 
        if self.rect.top <= 0:
            self.direction.y *= -1
            self.rect.top = 0
        if self.rect.bottom >= WINDOW_HEIGHT:
            self.direction.y *= -1
            self.rect.bottom = WINDOW_HEIGHT
        
        if self.rect.right >= WINDOW_WIDTH or self.rect.left <= 0:
            self.update_score('player' if self.rect.x < WINDOW_WIDTH / 2 else 'opponent')
            self.reset()
        
    def reset(self):
        self.rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
        self.reset_time = pygame.time.get_ticks()
        
    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.wall_collision()
        self.move(dt)


class Opponent(Paddle):
    def __init__(self, groups, ball: Ball):
        super().__init__(groups)
        self.rect.center = POS['opponent']
        self.old_rect = self.rect.copy()
        self.speed = SPEED['opponent']
        self.ball = ball
        
    def input(self):
        if self.ball.rect.centerx < WINDOW_WIDTH - WINDOW_WIDTH//2:
            self.speed = SPEED['opponent']
        else:
            self.speed = SPEED['opponent']//2
            
        
        self.direction.y = 1 if self.rect.centery < self.ball.rect.centery else -1

            