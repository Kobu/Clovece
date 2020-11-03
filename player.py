import figurine


class Player:
    def __init__(self, name):
        self.name = name

        self.color = None
        self.top_square = None
        self.start_square = None
        self.letter = None

        # self.figurines = self.create_figurines()

    def create_figurines(self):
        self.figurines = [figurine.Figurine(self.name, self.letter) for i in range(4)]

    def has_figurine_out(self):
        for figurine in self.figurines:
            if figurine.position is not None or not figurine.home:
                return figurine
        return False

    def pick_figurine(self):
        number = int(input())
        return self.figurines[number]
