import figurine


class Player:
    def __init__(self, name):
        self.name = name

        # TODO this needs restructuring
        self.color = None

        self.top_square = None
        self.start_square = None

        self.fig_symbol = None
        self.figurines = None

        # self.figurines = self.create_figurines()

    def create_figurines(self, amount):
        return [figurine.Figurine(self.name, self.fig_symbol, self.top_square, self.start_square) for _ in range(amount)]

    def has_figurine_out(self):
        for figurine in self.figurines:
            if figurine.position is not None or not figurine.home:
                return True
        return False

    def draw_fig_from_home(self):
        for figurine in self.figurines:
            if figurine.position is None:
                return figurine

    def has_finished(self):
        return all([figurine.home for figurine in self.figurines])

    def get_active_figurines(self):
        return [figurine for figurine in self.figurines if figurine.position is not None]
