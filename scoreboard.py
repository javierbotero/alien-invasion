import pygame
import pygame.font

from ship import Ship

class Scoreboard:
    """Class to manage the scoreboard"""
    def __init__(self, ai_game):
        """Creates a scoreboard object"""
        self.game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = ai_game.rect
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Create the text features
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

    def _prep_score(self):
        """Prepares the score image"""
        self.score_image = self._create_image(self.stats.score)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 40
        self.score_rect.y = 40

    def _prep_high_score(self):
        """Creates the high score image"""
        self.high_score = self._create_image(self.stats.high_score)
        self.high_score_rect = self.high_score.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 40

    def _prep_level(self):
        """Creates the level image"""
        self.level_image = self._create_image(self.stats.level, False)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 20

    def _prep_ships_left(self):
        """Creates the ships left image"""
        self.ships = pygame.sprite.Group()

        for n in range(self.stats.ships_left):
            ship = Ship(self.game)
            ship.image = pygame.transform.scale(ship.image, (40, 40))
            ship.rect = ship.image.get_rect()
            ship.rect.x = 20 + (n * 20) + (n * ship.rect.width)
            ship.rect.y = 10
            self.ships.add(ship)

    def blit_score_board(self):
        """blits the score to the game screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def _create_image(self, number, rounded=True):
        """Creates the text image"""
        num = round(number, -1) if rounded else number
        str_num = "{:,}".format(num) if rounded else str(num)
        image = self.font.render(
            str_num,
            True,
            self.text_color,
            self.settings.bg_color
            )
        return image

    def check_scores(self):
        """Checks if the score is high"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self._prep_high_score()

    def prep_items(self):
        """Prepares the scoreboard items"""
        self._prep_score()
        self._prep_high_score()
        self._prep_level()
        self._prep_ships_left()
