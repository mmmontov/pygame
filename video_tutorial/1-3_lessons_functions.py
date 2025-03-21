import pygame

pygame.init()
screen = pygame.display.set_mode((600, 300))
pygame.display.set_caption('Misha')
icon = pygame.image.load('images/icon.jpg')
pygame.display.set_icon(icon)
screen.fill((119, 168, 50))

square = pygame.Surface((50, 170))
square.fill('Blue')


myfont = pygame.font.Font('fonts/PlaywriteITModerna-Light.ttf', 40)
text_surface = myfont.render('hello, daun', True, 'black')


player = pygame.image.load('images/icon.jpg')


running = True
while running:

    screen.blit(player, (0, 0))
    screen.blit(square, (110, 0))
    screen.blit(text_surface, (300, 100))

    pygame.draw.circle(screen, 'Red', (250, 250), 30)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        
        
        
# elif event.type == pygame.KEYDOWN:
#     if event.key == pygame.K_a:
#         screen.fill((122, 64, 10))
    

