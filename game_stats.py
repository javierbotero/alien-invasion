class GameStats:
    def __init__(self, ai_game):
        """Initialize statistics"""
        self.settings = ai_game.settings
        self.file_hs = 'high_score.txt'
        self.initial_high_score = self._read_high_score()
        self.high_score = self.initial_high_score
        self._reset_settings()

    def _reset_settings(self):
        """Sets up the settings"""
        self.ships_left = self.settings.ships_limit
        self.game_active = False
        self.score = 0
        self.level = 0

    def _read_high_score(self):
        """Reads the high score from the file"""
        try:
            with open(self.file_hs) as file:
                return int(file.read())
        except FileNotFoundError:
            return 0

    def save_high_score(self):
        """Writes the high score to the file"""
        if self.high_score > self.initial_high_score:
            with open(self.file_hs, 'w') as file:
                file.write(str(self.high_score))
