import sys
from time import sleep
import random

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from energy import Energy

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
        self.rect = self.screen.get_rect()
        pygame.display.set_caption("Javier's Alien Invasion")
        self.ship = Ship(self)
        self.stats = GameStats(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.energies = pygame.sprite.Group()
        self._create_fleet()
        self.play_button = Button(
            self, "Play",
            200, 50, (self.rect.centery - 100)
            )
        self.medium_button = Button(
            self, "Medium",
            200, 50, self.rect.centery
            )
        self.hard_button = Button(
            self, "Hard",
            200, 50, (self.rect.centery + 100))
        self.sb = Scoreboard(self)

    def run_game(self):
        """Runs the game"""
        while True:
            self._check_events()
            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._close_game()
            elif event.type == pygame.KEYDOWN:
                self._update_keydown(event)
            elif event.type == pygame.KEYUP:
                self._update_keyup(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                self._check_click(position)

    def _check_click(self, position):
        """Respond to mouse clicks."""
        if (self.play_button.rect.collidepoint(position)
            and not self.stats.game_active):
            self._set_initial_speed(1, 1, 1, 8)
            self.sb.prep_items()
        elif (self.medium_button.rect.collidepoint(position)
              and not self.stats.game_active):
            self._set_initial_speed(1.5, 1.5, 1.5, 6)
            self.sb.prep_items()
        elif (self.hard_button.rect.collidepoint(position)
              and not self.stats.game_active):
            self._set_initial_speed(2, 2, 2, 4)
            self.sb.prep_items()

    def _set_initial_speed(self, alien, bullet, ship, modulus):
        """Sets the initial speed."""
        self.settings.initial_alien_speed = alien
        self.settings.initial_bullet_speed = bullet
        self.settings.initial_ship_speed = ship
        self.settings.initial_modulus_energies = modulus
        self._start_game()

    def _start_game(self):
        """Starts the game"""
        self.stats._reset_settings()
        self.stats.game_active = True

        # resets ship, aliens fleet and bullets
        self.ship.center_ship()
        self.aliens.empty()
        self.bullets.empty()
        self._create_fleet()
        self.settings._initialize_dynamic_settings()

        # hides cursor
        pygame.mouse.set_visible(False)

    def _update_screen(self):
        """Update the screen per iteration."""
        self.screen.fill(self.settings.bg_color)
        if self.stats.game_active:
            self._update_ship()
            self._update_aliens()
            self.aliens.draw(self.screen)
            self._update_bullets()
            self._create_energy()
            self._update_energy()
            self.sb.blit_score_board()
        else:
            self.play_button.draw_button()
            self.medium_button.draw_button()
            self.hard_button.draw_button()

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
            self._close_game()
        elif event.key == pygame.K_p:
            if not self.stats.game_active:
                self._start_game()

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
        """Update position of bullets and get rid of old bullets.
        Delete aliens and bullets too"""
        self.bullets.update()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        """Checks for collision of bullets and aliens"""
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
            )

        if collisions:
            for aliens in collisions.values():
                self.stats.score += int(self.settings.score_gain *
                                        self.settings.score_incrementor)
                self.sb._prep_score()

            self.sb.check_scores()

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb._prep_level()

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

    def _update_ship(self):
        """Updates ship and checks collisions"""
        if (pygame.sprite.spritecollideany(self.ship, self.aliens)
                or pygame.sprite.spritecollideany(self.ship, self.energies)
                or self._check_aliens_reach_bottom()):
            self._reset_game()
            if self.stats.ships_left <= 0:
                self.stats.game_active = False
                pygame.mouse.set_visible(True)
        else:
            self.ship.update()
            self.ship.blitme()

    def _reset_game(self):
        """resets game"""
        self.ship.center_ship()
        self.bullets.empty()
        self.aliens.empty()
        self.energies.empty()
        self.stats.ships_left -= 1
        self._create_fleet()
        self.sb._prep_ships_left()
        sleep(0.5)

    def _create_alien(self, index_x, index_y):
        """Create a new alien and add it to the alien group."""
        alien = Alien(self)
        width, height = alien.rect.size
        alien.x += width * 2 * index_x
        alien.rect.x = alien.x
        alien.rect.y += height * 2 * index_y
        self.aliens.add(alien)

    def _update_aliens(self):
        """Update the position of aliens."""
        self._check_fleet_edges()
        self.aliens.update()

    def _check_fleet_edges(self):
        """Checks if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_alien_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Changes alien's fleet direction and drops down the aliens"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.drop_alien_speed

        self.settings.fleet_direction *= -1

    def _check_aliens_reach_bottom(self):
        """Checks if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                return True

    def _close_game(self):
        """Saves high score to file and closes the game"""
        self.stats.save_high_score()
        sys.exit()

    def _create_energy(self):
        if (self.aliens and self.stats.game_active and
                (len(self.energies.sprites()) <
                int(self.settings.energies_allowed)) and
                (len(self.aliens.sprites()) %
                self.settings.modulus_energies == 0)):
            index = random.randint(0, len(self.aliens.sprites()) - 1)
            alien = self.aliens.sprites()[index]
            energy = Energy(self, alien)
            self.energies.add(energy)

    def _update_energy(self):
        """Updates energies position"""
        self.energies.update()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
