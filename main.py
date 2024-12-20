import pygame
import sys
import random

#Inicia o jogo
pygame.init()

#Configuração de tela
width, height = 400, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird")

# cria o objeto clock que permite controlar o FPS
clock = pygame.time.Clock()
FPS = 60

#Cores
blue = (0, 0, 255)
green = (0, 200, 0)
black = (0, 0 , 0)
white = (255, 255, 255)
red = (255, 0, 0)

#Criando o pássaro
bird_x = 50
bird_y = height // 2
bird_radius = 15
gravity = 0.6
bird_velocity = 0
jump_strength = -10

#Configuração dos canos
pipe_width = 50
pipe_gap = 120
pipe_velocity = 5
pipe_x = width
pipe_height = random.randint(100, height - pipe_gap -100)

#Fonte do Game Over
GO_font = pygame.font.Font(None, 64)

#Loop principal
running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            bird_velocity = jump_strength
    
    if not game_over:
    
        #Física do pássaro
        bird_velocity += gravity
        bird_y += bird_velocity

        #movimento dos canos
        pipe_x -= pipe_velocity
        if pipe_x + pipe_width < 0: 
            pipe_x = width
            pipe_height = random.randint(100, height - pipe_gap -100)

    #Colisão
        if (bird_y - bird_radius < 0 or bird_y + bird_radius > height or 
            (pipe_x < bird_x + bird_radius < pipe_x + pipe_width and 
            (bird_y - bird_radius < pipe_height or bird_y + bird_radius > pipe_height + pipe_gap))):
            game_over = True

    screen.fill((blue)) #Cor de fundo

    if not game_over: 

        #Desenho do pássaro
        pygame.draw.circle(screen, green, (bird_x, int(bird_y)), bird_radius)

        #desenho dos canos 
        pygame.draw.rect(screen, black, (pipe_x, 0, pipe_width, pipe_height)) #superior 
        pygame.draw.rect(screen, black, (pipe_x, pipe_height + pipe_gap, pipe_width, height - pipe_height -pipe_gap)) #inferior    
    else:
        game_over_text = GO_font.render("Game Over", True, red)
        screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - game_over_text.get_height() // 2))

    #Atualiza a tela
    pygame.display.flip()

    # Controla o FPS
    clock.tick(FPS)

pygame.quit()
sys.exit()