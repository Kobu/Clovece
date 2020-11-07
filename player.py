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

    def create_figurines(self):
        return [figurine.Figurine(self.name, self.fig_symbol) for i in range(4)]

    def has_figurine_out(self):
        for figurine in self.figurines:
            if figurine.position is not None or not figurine.home:
                return True
        return False

    def pick_figurine(self):
        number = int(input())
        return self.figurines[number]

    def draw_fig_from_home(self):
        for figurine in self.figurines:
            if figurine.position is None:
                return figurine

    def has_finished(self):
        result = []

        for figurine in self.figurines:
            if figurine.home: #or figurine.position is None:
                result.append(True)
            else:
                result.append(False)
        return all(result)
            # if not figurine.home:
            #     return False
        # return True

    def get_active_figurines(self):
        return [figurine for figurine in self.figurines if figurine.position is not None]
