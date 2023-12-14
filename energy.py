import random
import pygame
from pygame.sprite import Sprite

class Energy(Sprite):
    """A class to represent the energy."""
    def __init__(self, ai_game, alien):
        """Initialize the energy and set its starting position."""
        super().__init__()
        image = pygame.image.load('images/energy.bmp')
        self.image = pygame.transform.scale(image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.centerx = alien.rect.centerx
        self.rect.bottom = alien.rect.bottom
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.game = ai_game

    def update(self):
        """Updates position of the energy."""
        self.delete_energy()
        self.rect.y += self.game.settings.energy_speed

        if self.rect.x <= 0:
            self.rect.x += 1
        elif self.rect.right >= self.screen_rect.right:
            self.rect.x -= 1
        else:
            self.rect.x += random.randint(-1, 1)

        self.screen.blit(self.image, self.rect)

    def delete_energy(self):
        """Deletes energy when it goes off screen."""
        if self.rect.y >= self.screen_rect.bottom:
            self.game.energies.remove(self)