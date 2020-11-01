
class Figurine:
    def __init__(self, owner, position, name):
        self.owner = owner
        self.position = position
        self.home = False
        self.name = name

    def set_pos(self, coords):
        self.position = coords

    def in_home(self):
        self.home = True

    def remove_from_board(self):
        self.position = None
