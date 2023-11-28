class Settings:
    """A class to store all settings for Alien Invasion"""
    def __init__(self):
        self.screen_width = 1200
        self.screen_hight = 800
        self.bg_color = (0, 100, 230)
        self.speed_incrementor = 1.5
        self.bullet_speed = 1
        self.bullet_width = 3
        self.bullet_hight = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        self.alien_speed = 1
        self.fleet_direction = 1
        self.drop_alien_speed = 15
        self.ships_limit = 3
