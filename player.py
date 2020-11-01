
class Player:
    def __init__(self, color, name, figurines):
        self.name = name
        self.color = color
        self.figurines = figurines

    def set_top_square(self, coords):
        self.top_square = coords

    def set_start_square(self, coords):
        self.start_square = coords