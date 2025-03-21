import pygame

clock = pygame.time.Clock()

pygame.init()
icon = pygame.image.load('images/icon.jpg')
bg = pygame.image.load('images/background.jpg')
scaled_bg = pygame.transform.scale(bg, (bg.get_width() // 2, bg.get_height() // 2))
player_walk_right = [
    pygame.image.load('images/player_left/l1.png'),
    pygame.image.load('images/player_left/l2.png'),
    pygame.image.load('images/player_left/l3.png'),
    pygame.image.load('images/player_left/l4.png'),
]
player_walk_left = [
    pygame.image.load('images/player_right/r1.png'),
    pygame.image.load('images/player_right/r2.png'),
    pygame.image.load('images/player_right/r3.png'),
    pygame.image.load('images/player_right/r4.png'),
]
player_direction = player_walk_right

bg_sound = pygame.mixer.Sound('sounds/background.mp3')

player_anim_count = 0
bg_x = 0

player_speed = 5
player_x = 150
player_y = 356

is_jump = False
jump_count = 7

screen = pygame.display.set_mode(scaled_bg.get_size())
pygame.display.set_caption("Misha")
pygame.display.set_icon(icon)
bg_sound.set_volume(0.05)
bg_sound.play()

running = True

while running:
    keys = pygame.key.get_pressed()
    screen.blit(scaled_bg, (bg_x, 0))
    screen.blit(scaled_bg, (bg_x + scaled_bg.get_width(), 0))
    
    if keys[pygame.K_RIGHT]:
        player_direction = player_walk_right
    elif keys[pygame.K_LEFT]:
        player_direction = player_walk_left

    screen.blit(player_direction[player_anim_count], (player_x, player_y))


    if keys[pygame.K_LEFT] and player_x > 10:
        player_x -= player_speed
    elif keys[pygame.K_RIGHT] and player_x < screen.get_width()-50:
        player_x += player_speed

    if not is_jump:
        if keys[pygame.K_UP]:
            is_jump = True  
    else:
        if jump_count >= -7:
            if jump_count > 0:
                player_y -= (jump_count**2) / 2
            else:
                player_y += (jump_count**2) / 2
            jump_count -= 1
        else: 
            is_jump = False
            jump_count = 7


    if player_anim_count < 3:
        player_anim_count += 1
    else:
        player_anim_count = 0
    bg_x -= 2
    if bg_x == -scaled_bg.get_width():
        bg_x = 0
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
    
    clock.tick(50)

