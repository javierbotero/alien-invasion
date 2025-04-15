import pytest

from alien_invasion import AlienInvasion
from alien import Alien
from energy import Energy

@pytest.fixture(scope="session")
def game():
    return AlienInvasion()

@pytest.fixture
def alien(game):
    return Alien(game)

@pytest.fixture
def energy(game, alien):
    return Energy(game, alien)