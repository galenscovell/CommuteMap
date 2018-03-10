"""
Takes in generated values and plots them into a graphical representation.

@Author GalenS <galen.scovell@gmail.com>
"""

import math
import pygame
import sys

from models.distance_matrix import DistanceMatrix
from models.location import Location

import util.constants as constants


class Visualizer:
    def __init__(self, focus_location):
        self.map_width = math.ceil((constants.window_x / 360.0) * (180 + focus_location['width']))
        self.map_height = math.ceil((constants.window_y / 180.0) * (90 - focus_location['width']))

        grid = self.create_grid()

        pygame.init()
        screen = pygame.display.set_mode((constants.window_x, constants.window_y))
        pygame.display.set_caption("Commute Mapper")
        screen.fill(constants.c_background)

        running = True
        frames = 0
        while running:
            frames += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    None

            if frames > constants.update_ticks:
                frames = 0
                self.update_grid(grid, screen)

            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def create_grid(self):
        grid = []
        for y in range(0, self.map_height):
            grid.append([])
            for x in range(0, self.map_width):
                grid[y].append(0)

        return grid

    def update_grid(self, grid, screen):
        for y in range(0, self.map_height):
            for x in range(0, self.map_width):
                color = constants.c_cell
                pygame.draw.rect(
                    screen, color,
                    [
                        (constants.margin + constants.cell_size) * x + constants.margin,
                        (constants.margin + constants.cell_size) * y + constants.margin,
                        constants.cell_size, constants.cell_size
                    ]
                )
