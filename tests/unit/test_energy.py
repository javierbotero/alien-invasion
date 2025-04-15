import pytest
from energy import Energy

class TestEnergy:
    def test_update(self, energy):
        """test energy 'y' position"""
        initial_position = 0
        energy.rect.y = initial_position
        energy.update()
        assert energy.rect.y == initial_position + energy.game.settings.energy_speed

    def test_delete_energy(self, energy):
        """test energy deletion"""
        energy.rect.y += energy.game.rect.bottom
        energy.update()
        assert len(energy.game.energies.sprites()) == 0
