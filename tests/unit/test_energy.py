import pytest
from energy import Energy

class TestEnergy:
    def test_update(self, energy):
        """test energy 'y' position"""
        initial_position = 0
        energy.rect.y = initial_position
        energy.update()
        assert energy.rect.y == initial_position + energy.game.settings.energy_speed
