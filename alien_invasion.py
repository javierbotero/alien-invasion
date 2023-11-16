import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet

class AlienInvasion:
    """A class to represent the Alien Invasion"""
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (
                self.settings.screen_width,
                self.settings.screen_hight
            ))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_hight = self.screen.get_rect().height
        pygame.display.set_caption("Javier's Alien Invasion")
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

    def run_game(self):
        """Runs the game"""
        while True:
            self._check_events()
            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._update_keydown(event)
            elif event.type == pygame.KEYUP:
                self._update_keyup(event)

    def _update_screen(self):
         """Update the screen per iteration."""
         self.screen.fill(self.settings.bg_color)
         self.ship.update()
         self.ship.blitme()
         self.bullets.update()
         for bullet in self.bullets.sprites():
             bullet.draw_bullet()

         pygame.display.flip()

    def _update_keydown(self, event):
        """Updates keydown events."""
        if event.key == pygame.K_RIGHT:
            self.ship.move_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.move_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _update_keyup(self, event):
        """Updates keyup events."""
        if event.key == pygame.K_RIGHT:
            self.ship.move_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.move_left = False

    def _fire_bullet(self):
        bullet = Bullet(self)
        self.bullets.add(bullet)

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
