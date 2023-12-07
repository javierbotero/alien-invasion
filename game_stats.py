class GameStats:
    def __init__(self, ai_game):
        """Initialize statistics"""
        self.settings = ai_game.settings
        self.high_score = 0
        self._reset_settings()

    def _reset_settings(self):
        """Sets up the settings"""
        self.ships_left = self.settings.ships_limit
        self.game_active = False
        self.score = 0
        self.level = 0