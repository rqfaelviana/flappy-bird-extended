import pygame
import sys
import random

#Inicia o jogo
pygame.init()

#inicia o mixer de sons
pygame.mixer.init()

#Efeitos sonoros 
fly = pygame.mixer.Sound("sounds/whoosh.mp3")
point = pygame.mixer.Sound("sounds/point.mp3")
slam = pygame.mixer.Sound("sounds/slam.mp3")
gameover_sound = pygame.mixer.Sound("sounds/game_over.mp3")

#Imagens
background = pygame.image.load("images/background.png")
rowlet = pygame.image.load("images/rowlet_1.png")
pipe_img = pygame.image.load("images/pipe.png")



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

#Fonte do Game Over
GO_font = pygame.font.Font(None, 64)

#Criando o pássaro
bird_x = 50
bird_y = height // 2
gravity = 0.6
bird_velocity = 0
jump_strength = -10

#Configuração dos canos
pipe_width = 50
pipe_gap = 120
pipe_velocity = 5
pipe_x = width
pipe_height = random.randint(100, height - pipe_gap -100)

# Redimensiona as imagens
rowlet = pygame.transform.scale(rowlet, (40,30))
pipe_img = pygame.transform.scale(pipe_img, (pipe_width, height))

#variáveis de pontuação
score = 0
best_score = 0
point_awarded = False # evita múltiplos pontos por cano

#contagem inicial para os canos aparecerem
start_time = 0

# função para reiniciar o jogo
def reset_game():
    global bird_y, bird_velocity, pipe_x, pipe_height, game_over, score, best_score, point_awarded, game_started
    if score > best_score:
        best_score = score

    bird_y = height // 2
    bird_velocity = 0 
    pipe_x = width
    pipe_height = random.randint(100, height - pipe_gap - 100)
    game_over = False
    score = 0 
    point_awarded = False
    game_started = False

#Loop principal
running = True
game_over = False
game_started = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not game_started:
                game_started = True
                start_time = pygame.time.get_ticks()
            else:
                bird_velocity = jump_strength 
                fly.play() 
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r: 
                reset_game()
    
    if game_started and not game_over:
        current_time = pygame.time.get_ticks()

        if current_time - start_time >= 4000:
            pipe_x -= pipe_velocity
        #Física do pássaro
        bird_velocity += gravity
        bird_y += bird_velocity

        #Aumenta a pontuação quando passa pelo cano
        if pipe_x + pipe_width < bird_x and not point_awarded:
            score += 1
            point_awarded = True
            point.play()

        #movimento dos canos
        if pipe_x + pipe_width < 0: 
            pipe_x = width
            pipe_height = random.randint(100, height - pipe_gap -100)
            point_awarded = False

    #Colisão
        bird_rect = pygame.Rect(bird_x, bird_y, 40, 30)
        pipe_top_rect = pygame.Rect(pipe_x, pipe_height - height, pipe_width, height)
        pipe_bottom_rect = pygame.Rect(pipe_x, pipe_height + pipe_gap, pipe_width, height)
        
        if bird_y < 0 or bird_y + 55 > height or bird_rect.colliderect(pipe_top_rect) or bird_rect.colliderect(pipe_bottom_rect):
            game_over = True
            slam.play()
            gameover_sound.play()

        if score > best_score:
            best_score = score

    #Desenha o fundo
    screen.blit(background, (0,0))

    if not game_over: 

        #Desenho do pássaro
        screen.blit(rowlet, (bird_x, int(bird_y)))

        #desenho dos canos 
        screen.blit(pipe_img, (pipe_x, pipe_height - height)) # superior
        screen.blit(pipe_img, (pipe_x, pipe_height + pipe_gap)) # inferior

    else:
        game_over_text = GO_font.render("Game Over", True, red)
        restart_text = GO_font.render("Press R to Restart", True, white)
        screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - game_over_text.get_height() // 2- 50))
        screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 - restart_text.get_height() // 2 + 20))

        # Exibe sua maior pontuação 
        best_score_text = GO_font.render(f"Best score: {best_score}", True, white)
        screen.blit(best_score_text, (width // 2 - best_score_text.get_width() // 2, 60))

    # Exibe a pontuação atual
    score_text = GO_font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (width // 2 - score_text.get_width() // 2, 20))
 
    #Atualiza a tela
    pygame.display.flip()

    # Controla o FPS
    clock.tick(FPS)

pygame.quit()
sys.exit()