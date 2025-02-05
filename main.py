import pygame
import sys
import random
import time

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
rowlet = [
    pygame.image.load("images/rowlet_1.png"),
    pygame.image.load("images/rowlet_2.png"),
    pygame.image.load("images/rowlet_3.png"),
    pygame.image.load("images/rowlet_4.png"),
]
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
rowlet_resized = [pygame.transform.scale(frame, (40,30)) for frame in rowlet]
pipe_img = pygame.transform.scale(pipe_img, (pipe_width, height))

# Variáveis de animação
current_frame = 0 
animation_speed = 10
frame_counter = 0

#variáveis de pontuação
score = 0
best_score = 0
point_awarded = False # evita múltiplos pontos por cano

#contagem inicial para os canos aparecerem
start_time = 0

def draw_text_zoom(text, font, color, x, y, scale_factor=1.5):
    #cria a superfícia do texto
    text_surface = font.render(text, True, color)

    #aumenta o tamanho do texto para o efeito de zoom
    width = int(text_surface.get_width() * scale_factor)
    height = int(text_surface.get_height() * scale_factor)
    text_surface = pygame.transform.scale(text_surface, (width, height))

    screen.blit(text_surface, (x - width // 2, y - height // 2))

def draw_button(text, font, color, x, y, height, action=None):
    # Calcula o tamanho do texto
    button_text = font.render(text, True, black)
    text_width, text_height = button_text.get_width(), button_text.get_height()

    button_width = text_width + 20 
    button_rect = pygame.Rect(x - button_width // 2, y - height // 2, button_width, height)

    # Efeito de hover
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (150, 150, 255), button_rect)
    else:
        pygame.draw.rect(screen, color, button_rect)

    # Desenha o texto no botão
    screen.blit(button_text, (x - text_width // 2, y - text_height // 2))

    # Ação do botão 
    if pygame.mouse.get_pressed()[0] and button_rect.collidepoint(mouse_pos):
        if action:
            action()

# função para reiniciar o jogo
def reset_game():
    global bird_y, bird_velocity, pipe_x, pipe_height, game_over, score, best_score, point_awarded, game_started
    if score > best_score:
        best_score = score

    time.sleep(1)

    bird_y = height // 2
    bird_velocity = 0 
    pipe_x = width
    pipe_height = random.randint(100, height - pipe_gap - 100)
    game_over = False
    score = 0 
    point_awarded = False
    game_started = False

def restart_game():
    reset_game()
    global game_over
    game_over = False

def quit_game():
    pygame.quit()
    sys.exit()

#Loop principal
running = True
game_over = False
game_started = False

while running:
    frame_counter += 1
    if frame_counter >= animation_speed:
        frame_counter = 0
        current_frame = (current_frame + 1) % len(rowlet) 
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
        #desenho do rowlet
        screen.blit(rowlet_resized[current_frame], (bird_x, int(bird_y)))

        #desenho dos canos 
        screen.blit(pipe_img, (pipe_x, pipe_height - height)) # superior
        screen.blit(pipe_img, (pipe_x, pipe_height + pipe_gap)) # inferior

    else:
        draw_text_zoom("Game Over", GO_font, red, width // 2, height // 2 - 50)
        draw_button("Reiniciar", GO_font, white, width // 2, height // 2 + 20, 50, restart_game)
        draw_button("Sair", GO_font, white, width // 2, height // 2 + 100, 50, quit_game)


    # Exibe a maior pontuação
        #game_over_text = GO_font.render("Game Over", True, red)
        #restart_text = GO_font.render("Press R to Restart", True, white)
        #screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - game_over_text.get_height() // 2- 50))
        #screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 - restart_text.get_height() // 2 + 20))

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