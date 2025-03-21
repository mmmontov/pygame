import pygame
import random

image_path = '/data/data/com.misha.myapp/files/app/'

clock = pygame.time.Clock()

pygame.init()

bg = pygame.image.load(image_path+'images/background.jpg')
scaled_bg = pygame.transform.scale(bg, (bg.get_width() // 2, bg.get_height() // 2))
screen = pygame.display.set_mode(scaled_bg.get_size())
icon = pygame.image.load(image_path+'images/icon.jpg')
ghost = pygame.image.load(image_path+'images/ghost.png').convert_alpha()
bullet = pygame.image.load(image_path+'images/bullet.png').convert_alpha()


player_walk_right = [
    pygame.image.load(image_path+'images/player_left/l1.png').convert_alpha(),
    pygame.image.load(image_path+'images/player_left/l2.png').convert_alpha(),
    pygame.image.load(image_path+'images/player_left/l3.png').convert_alpha(),
    pygame.image.load(image_path+'images/player_left/l4.png').convert_alpha(),
]
player_walk_left = [
    pygame.image.load(image_path+'images/player_right/r1.png').convert_alpha(),
    pygame.image.load(image_path+'images/player_right/r2.png').convert_alpha(),
    pygame.image.load(image_path+'images/player_right/r3.png').convert_alpha(),
    pygame.image.load(image_path+'images/player_right/r4.png').convert_alpha(),
]
player_direction = player_walk_right

bg_sound = pygame.mixer.Sound(image_path+'sounds/background.mp3')


floor_y = 356


player_anim_count = 0
bg_x = 0

player_speed = 5
player_x = 150
player_y = floor_y

is_jump = False
jump_count = 7


ghost_x = 1000
ghost_y = floor_y + 20
ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 5000)
ghost_list_in_game = []


bullets = []
bullets_left = 5

label = pygame.font.Font(image_path+'fonts/PlaywriteITModerna-Light.ttf', 60)
lose_label = label.render('GAME OVER', False, (193, 196, 199))
restart_label = label.render('restart', False, (115, 132, 148))
restart_label_rect = restart_label.get_rect(topleft=(300, 300))


pygame.display.set_caption("Misha")
pygame.display.set_icon(icon)
bg_sound.set_volume(0.05)
bg_sound.play()

gameplay = True
running = True

while running:
    keys = pygame.key.get_pressed()
    screen.blit(scaled_bg, (bg_x, 0))
    screen.blit(scaled_bg, (bg_x + scaled_bg.get_width(), 0))
    
    if gameplay:
        player_rect = player_walk_left[0].get_rect(topleft=(player_x, player_y))
        
        
        if ghost_list_in_game:
            for i, el in enumerate(ghost_list_in_game):
                screen.blit(ghost, el)
                el.x -= 8

                if el.x == 0:
                    ghost_list_in_game.pop(i)
                
                if player_rect.colliderect(el):
                    gameplay = False
        
        
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
            
            
           
        if bullets:
            for i, el in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                
                el.x += 10

                if el.x > 1000:
                    bullets.pop(i)
                    
                if ghost_list_in_game:
                    for i, gh in enumerate(ghost_list_in_game):
                        if el.colliderect(gh):
                            ghost_list_in_game.pop(i)
                            bullets.pop(i)
        
    else:
        screen.fill((87, 88, 89))
        screen.blit(lose_label, (200, 200))
        screen.blit(restart_label, restart_label_rect)
        
        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            ghost_list_in_game.clear()
            bullets.clear()
            bullets_left = 5

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == ghost_timer:
            ghost_list_in_game.append(ghost.get_rect(topleft=(ghost_x, ghost_y)))
            pygame.time.set_timer(ghost_timer, random.randint(2000, 5000))
        if gameplay and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and bullets_left > 0:
            bullets.append(bullet.get_rect(topleft=(player_x+10, player_y+20)))
            bullets_left -= 1
            
    
    clock.tick(25)

