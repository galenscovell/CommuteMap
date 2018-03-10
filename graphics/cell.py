

class Cell:
    def __init__(self, grid_x, grid_y, pixel_x, pixel_y):
        self.id = -1
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.pixel_x = pixel_x
        self.pixel_y = pixel_y
        self.address = None
        self.duration = 0.0

    def set_address(self, address):
        self.address = address

    def set_duration(self, duration):
        self.duration = duration // 60

    def get_duration_color(self):
        c = self.duration / (120 / 255)
        return c
