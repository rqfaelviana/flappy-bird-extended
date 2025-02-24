import pygame 
import random

class Pipe:
    def __init__(self, x, width=50, gap=120, speed=5, screen_height=600):
        self.x = x
        self.width = width
        self.gap = gap
        self.speed = speed
        self.screen_height = screen_height
        self.pipe_img = pygame.image.load("images/pipe.png")
        self.pipe_img = pygame.transform.scale(self.pipe_img, (self.width, self.screen_height))
        self.reset_pipe()

    def reset_pipe(self):
        self.height = random.randint(100, self.screen_height - self.gap - 100)
        self.passed = False #evitar contar múltiplos pontos para o mesmo cano
    
    def update(self):
        self.x -= self.speed
        if self.x + self.width < 0: # se o cano sair da tela, reposiciona
            self.x = 400
            self.reset_pipe()
    
    def draw(self, screen):
        screen.blit(self.pipe_img, (self.x, self.height - self.screen_height)) #cano superior
        screen.blit(self.pipe_img, (self.x, self.height + self.gap)) #cano inferior
    
    def get_rects(self):
        return (
            pygame.Rect(self.x, self.height - self.screen_height, self.width, self.screen_height),
            pygame.Rect(self.x, self.height + self.gap, self.width, self.screen_height),
        )