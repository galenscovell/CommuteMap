"""
Takes in generated values and plots them into a graphical representation.

@Author GalenS <galen.scovell@gmail.com>
"""

import math
import pygame
import sys

from models.distance_matrix import DistanceMatrix
from models.location import Location

from graphics.cell import Cell

import util.constants as constants


class Visualizer:
    def __init__(self, origins, destinations, distance_matrix):
        self.rows, self.columns, self.x_offset, self.y_offset = self.find_map_bounds(origins, destinations)
        self.map_width = self.columns * (constants.cell_size + constants.margin)
        self.map_height = self.rows * (constants.cell_size + constants.margin)
        print('Map dimensions: [{0}, {1}], [{2}, {3}]'.format(self.columns, self.rows, self.map_width, self.map_height))

        if self.map_width > 1280 or self.map_height > 960:
            print('Map dimensions too large -- tool isn\'t designed for cross country trips!')
            sys.exit()

        grid = self.create_grid(origins, destinations, distance_matrix)

        # Init screen
        pygame.init()
        self.font = pygame.font.SysFont("source code pro", 12)
        screen = pygame.display.set_mode((self.map_width, self.map_height))
        pygame.display.set_caption("Commute Mapper")
        screen.fill(constants.c_background)
        clock = pygame.time.Clock()

        # Main loop
        running = True
        while running:
            clock.tick(constants.frame_rate)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    None

            screen.fill(constants.c_background)
            self.update_grid(grid, screen)

            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def create_grid(self, origins, destinations, distance_matrix):
        grid = []
        for y in range(0, self.rows):
            grid.append([])
            for x in range(0, self.columns):
                grid[y].append(
                    Cell(
                        x, y,
                        x * (constants.cell_size + constants.margin),
                        y * (constants.cell_size + constants.margin)
                    )
                )

        for o in range(0, len(origins)):
            if len(origins) > 1:
                self.set_origin(origins[o], grid, distance_matrix[o])
            else:
                self.set_origin(origins[o], grid)

        for d in range(0, len(destinations)):
            if len(destinations) > 1:
                self.set_destination(destinations[d], grid, distance_matrix[d])
            else:
                self.set_destination(destinations[d], grid)

        return grid

    def update_grid(self, grid, screen):
        labels = []
        for y in range(0, self.rows):
            for x in range(0, self.columns):
                cell = grid[y][x]

                if cell.id == constants.origin_id:
                    color = (cell.get_duration_color(), 128, 128)
                    label = [(cell.address, 1, (255, 255, 0)), (cell.pixel_x + 4, cell.pixel_y - 8)]
                    labels.append(label)

                    duration_label = [('{0}min'.format(cell.duration), 1, (255, 255, 255)), (cell.pixel_x + 4, cell.pixel_y + 14)]
                    labels.append(duration_label)
                elif cell.id == constants.destination_id:
                    color = constants.c_destination
                    label = [(cell.address, 1, (255, 0, 255)), (cell.pixel_x + 4, cell.pixel_y - 8)]
                    labels.append(label)
                else:
                    color = constants.c_empty

                pygame.draw.rect(
                    screen, color,
                    [
                        (constants.margin + constants.cell_size) * cell.grid_x + constants.margin,
                        (constants.margin + constants.cell_size) * cell.grid_y + constants.margin,
                        constants.cell_size, constants.cell_size
                    ]
                )

        for l in labels:
            text = self.font.render(l[0][0], l[0][1], l[0][2])
            screen.blit(text, (l[1][0] - text.get_width() / 2, l[1][1] - text.get_height() / 2))
        labels.clear()

    def set_origin(self, location, grid, distance_entry=None):
        x, y = self.convert_geo_to_coords(location['center'][0], location['center'][1])
        x -= self.x_offset
        y -= self.y_offset

        grid[x][y].set_address(location['label'])
        grid[x][y].id = constants.origin_id

        nex, ney = self.convert_geo_to_coords(location['northeast'][0], location['northeast'][1])
        nex -= self.x_offset
        ney -= self.y_offset
        half_height = int(math.fabs((ney - y) / 2))
        half_width = int(math.fabs((nex - x) / 2))

        if distance_entry:
            grid[x][y].set_duration(distance_entry['duration'])

    def set_destination(self, location, grid, distance_entry=None):
        x, y = self.convert_geo_to_coords(location['center'][0], location['center'][1])
        x -= self.x_offset
        y -= self.y_offset

        grid[x][y].set_address(location['label'])
        grid[x][y].id = constants.destination_id

        if distance_entry:
            grid[x][y].set_duration(distance_entry['duration'])

    @staticmethod
    def convert_geo_to_coords(lat, lng):
        x = int(6371 * math.cos(lat) * math.cos(lng) / (constants.cell_size + constants.margin))
        y = int(6371 * math.cos(lat) * math.sin(lng) / (constants.cell_size + constants.margin))

        return x, y

    def find_map_bounds(self, origins, destinations):
        most_north = -math.inf
        most_east = -math.inf
        most_south = math.inf
        most_west = math.inf

        for loc in (origins + destinations):
            x, y = self.convert_geo_to_coords(loc['center'][0], loc['center'][1])

            if x > most_east:
                most_east = x
            if x < most_west:
                most_west = x

            if y > most_north:
                most_north = y
            if y < most_south:
                most_south = y

        width = int(math.fabs(most_east - most_west))
        height = int(math.fabs(most_north - most_south))

        return width + 20, height + 20, most_west - 10, most_south - 10
