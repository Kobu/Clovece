from coord_system import *


class Figurine:
    def __init__(self, owner, name):
        self.owner = owner
        self.name = name
        self.home = False

        self.position = None

    def set_pos(self, coords: Coords):
        self.position = coords

    def initialize_figurine(self, coords: Coords):
        self.position = coords

    def in_home(self):
        self.home = True

    def knockout_figurine(self):
        self.position = None
