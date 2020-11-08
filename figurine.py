class Figurine:
    def __init__(self, owner, name, top_square, start_square):
        self.owner = owner
        self.name = name

        self.top_square = top_square
        self.start_square = start_square

        self.home = False

        self.position = None

    def set_pos(self, coords):
        self.position = coords

    def in_home(self):
        self.home = True

    def knockout_figurine(self):
        self.position = None


