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
        self.animation_speed = 100 
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

        # Atualiza a animação com base no tempo
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.images)

    def draw(self, screen):
        angle = min(max(-self.velocity * 2, -20), 20)
        rotated_image = pygame.transform.rotate(self.images[self.current_frame], angle)
        screen.blit(rotated_image, (self.x, int(self.y)))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 40, 30)
    
    def jump(self): 
        self.velocity = self.jump_strength
