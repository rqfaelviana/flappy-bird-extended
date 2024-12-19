import pygame
import sys

#Inicia o jogo
pygame.init()

#Configuração de tela
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Flappy Bird")

# cria o objeto clock que permite controlar o FPS
clock = pygame.time.Clock()

#Cores
blue = (0, 0, 255)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((blue)) #Cor de fundo

    #Atualiza a tela
    pygame.display.flip()

    # Controla o FPS
    clock.tick(60)

pygame.quit()
sys.exit()