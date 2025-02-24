import pygame
import sys
import time
from bird import Bird
from pipe import Pipe

#inicia o jogo
pygame.init()
pygame.mixer.init()

#efeitos sonoros
fly = pygame.mixer.Sound("sounds/whoosh.mp3")
point = pygame.mixer.Sound("sounds/point.mp3")
slam = pygame.mixer.Sound("sounds/slam.mp3")
gameover_sound = pygame.mixer.Sound("sounds/game_over.mp3")

# Configuração da tela
width, height = 400, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
FPS = 60

#Cores
white = (255, 255, 255)
red = (255, 0, 0)

#Fonte
GO_font = pygame.font.Font(None, 64)

#Fundo
background = pygame.image.load("images/background.png")

#objetos do jogo
bird = Bird(50, height // 2)
pipe = Pipe(width)

score = 0
best_score = 0
game_over = False
game_started = False

def reset_game():
    global score, game_over, game_started, best_score
    if score > best_score:
        best_score = score
    time.sleep(1)
    bird.y = height // 2
    bird.velocity = 0
    pipe.x = width
    pipe.reset_pipe()
    score = 0
    game_over = False
    game_started = False

def quit_game():
    pygame.quit()
    sys.exit()

def game_events():
    global running, game_started, game_over

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not game_started:
                game_started = True
            elif not game_over:
                bird.jump()
                fly.play()

def game_logic():
    global game_over, score

    if game_started and not game_over:
        bird.update()
        pipe.update()

        if pipe.x + pipe.width < bird.x and not pipe.passed:
            score += 1
            pipe.passed = True
            point.play()

        bird_rect = bird.get_rect()
        pipe_top_rect, pipe_bottom_rect = pipe.get_rects()

        if bird.y < 0 or bird.y + 30 > height or bird_rect.colliderect(pipe_top_rect) or bird_rect.colliderect(pipe_bottom_rect):
            game_over = True
            slam.play()
            gameover_sound.play()

def draw_screen():
    screen.blit(background, (0, 0))
    
    if not game_over:
        bird.draw(screen)
        pipe.draw(screen)
    else:
        draw_text_zoom("Game Over", GO_font, red, width // 2, height // 2 - 50)
        draw_button("Reiniciar", GO_font, white, width // 2, height // 2 + 20, 50, reset_game)
        draw_button("Sair", GO_font, white, width // 2, height // 2 + 100, 50, quit_game)
    
    score_text = GO_font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (width // 2 - score_text.get_width() // 2, 20))
    
    pygame.display.flip()

def draw_text_zoom(text, font, color, x, y, scale_factor=1.5):
    text_surface = font.render(text, True, color)
    text_surface = pygame.transform.scale(text_surface, (int(text_surface.get_width() * scale_factor), int(text_surface.get_height() * scale_factor)))
    screen.blit(text_surface, (x - text_surface.get_width() // 2, y - text_surface.get_height() // 2))

def draw_button(text, font, color, x, y, height, action=None):
    button_text = font.render(text, True, (0, 0, 0))
    text_width, text_height = button_text.get_width(), button_text.get_height()
    button_width = text_width + 20
    button_rect = pygame.Rect(x - button_width // 2, y - height // 2, button_width, height)

    pygame.draw.rect(screen, color, button_rect)
    screen.blit(button_text, (x - text_width // 2, y - text_height // 2))

    if pygame.mouse.get_pressed()[0] and button_rect.collidepoint(pygame.mouse.get_pos()) and action:
        action()

# Loop principal
running = True
while running:
    game_events()
    game_logic()
    draw_screen()
    clock.tick(FPS)

pygame.quit()
sys.exit()
