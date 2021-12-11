import pygame

from src.constants import SPACE_SHIP_RED, LASER_RED, SPACE_SHIP_BLUE, LASER_BLUE, SPACE_SHIP_GREEN, LASER_GREEN
from src.lasers.Laser import Laser
from src.ships.Ship import Ship


class Enemy(Ship):
    COLOR_MAP = {
        'red': (SPACE_SHIP_RED, LASER_RED),
        'blue': (SPACE_SHIP_BLUE, LASER_BLUE),
        'green': (SPACE_SHIP_GREEN, LASER_GREEN)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health=health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 15, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1