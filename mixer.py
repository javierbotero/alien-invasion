import pygame

class Mixer:
    """A class to represent the Sounds"""
    def __init__(self):
        """Create a Mixer object"""
        self.fx_ship_shot = pygame.mixer.Sound("sounds/ship_shot.wav")
        self.fx_ship_shot.set_volume(0.3)
        self.fx_alien_shot = pygame.mixer.Sound("sounds/laser_gun.wav")
        self.start_music = "sounds/start_music.mp3"
        self.game_music = "sounds/game_music.mp3"
        self.playing_start_music = True
        self._play_music()

    def _play_music(self):
        """Unloads current music and starts the game music"""
        if self.playing_start_music:
            pygame.mixer.music.load(self.game_music)
        else:
            pygame.mixer.music.load(self.start_music)

        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        self.playing_start_music = not self.playing_start_music
