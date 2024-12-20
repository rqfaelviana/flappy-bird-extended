import pygame
import sys

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

#Criando o pássaro
bird_x = 50
bird_y = height // 2
bird_radius = 15
gravity = 0.3
bird_velocity = 0
jump_strength = -10

#Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            bird_velocity = jump_strength
    

    #Física do pássaro
    bird_velocity += gravity
    bird_y += bird_velocity

    screen.fill((blue)) #Cor de fundo

    #Desenho do pássaro
    pygame.draw.circle(screen, green, (bird_x, int(bird_y)), bird_radius)

    #Atualiza a tela
    pygame.display.flip()

    # Controla o FPS
    clock.tick(FPS)

pygame.quit()
sys.exit()