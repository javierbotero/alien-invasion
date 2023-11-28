import pygame

class Ship:
    """A simple attempt at making a ship."""
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.move_right = False
        self.move_left = False
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Updates position of ship"""
        if self.move_right and self.screen_rect.right > self.rect.right:
            self.x += self.settings.speed_incrementor

        if self.move_left and self.screen_rect.left < self.rect.left:
            self.x -= self.settings.speed_incrementor

        self.rect.x = self.x
    
    def center_ship(self):
        """Centers the ship"""
        self.rect.midbottom = self.screen_rect.midbottom
