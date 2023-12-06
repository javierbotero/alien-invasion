import pygame.font

class Button:
    def __init__(self, ai_game, msg, width, height, top):
        """Initialize button attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Create the button's properties.
        self.width, self.height = width, height
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Create the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = self.screen_rect.centerx
        self.rect.y = top

        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image."""
        self.text_image = self.font.render(
            msg,
            True,
            self.text_color,
            self.button_color
            )
        self.text_rect = self.text_image.get_rect()
        self.text_rect.center = self.rect.center

    def draw_button(self):
        """Draw blank button and then draw message."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.text_image, self.text_rect)
