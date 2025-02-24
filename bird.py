import pygame

class Bird:
    def __init__(self, x, y, gravity=0.6, jump_strength=-10):
        self.x = x 
        self.y = y
        self.gravity = gravity
        self.velocity = 0
        self.jump_strength = jump_strength
        self.images = [
            pygame.image.load("images/rowlet_1.png"),
            pygame.image.load("images/rowlet_2.png"),
            pygame.image.load("images/rowlet_3.png"),
            pygame.image.load("images/rowlet_4.png"),
        ]
        self.images = [pygame.transform.scale(img, (40, 30)) for img in self.images]
        self.current_frame = 0
        self.animation_speed = 10
        self.frame_counter = 0

    def jump(self):
        self.velocity = self.jump_strength

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

        #animação do pássaro
        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            self.frame_counter = 0 
            self.current_frame = (self.current_frame + 1) % len(self.images)
    
    def draw(self, screen):
        screen.blit(self.images[self.current_frame], (self.x, int(self.y)))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, 40, 30)
    
