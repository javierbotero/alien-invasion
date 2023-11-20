import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

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
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

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
        self.aliens.draw(self.screen)
        self._update_bullets()

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
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            bullet = Bullet(self)
            self.bullets.add(bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        self.bullets.update()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        print(f"Bullets: {len(self.bullets)}")

    def _create_fleet(self):
        """Creates the Alien's fleet"""
        alien = Alien(self)
        width, height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * width)
        number_aliens_x = available_space_x // (2 * width)
        available_space_y = (self.settings.screen_hight - (height * 3)
                               - self.ship.rect.height)
        number_aliens_y = available_space_y // (height * 2)

        for index_y in range(number_aliens_y):
            for index_x in range(number_aliens_x):
                self._create_alien(index_x, index_y)

    def _create_alien(self, index_x, index_y):
        """Create a new alien and add it to the alien group."""
        alien = Alien(self)
        width, height = alien.rect.size
        alien.x += width * 2 * index_x
        alien.rect.x = alien.x
        alien.rect.y += height * 2 * index_y
        self.aliens.add(alien)

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
