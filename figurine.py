
class Figurine:
    def __init__(self, owner, name):
        self.owner = owner
        self.name = name

        self.position = None
        self.home = False

    def set_pos(self, coords):
        self.position = coords

    def initialize_figurine(self, coords):
        self.position = coords

    def in_home(self):
        self.home = True

    def remove_from_board(self):
        self.position = None
