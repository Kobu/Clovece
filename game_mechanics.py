from coord_system import *


class GameMechanics:
    def __init__(self, board_size):
        self.board_size = board_size

        self.path = self.calculate_path()

    def calculate_path(self):
        start_coord = Coords(-(self.board_size // 2), 1)  # can be anything # TODO remove the negative
        amount_of_playing_squares = 4 * self.board_size - 4

        result = []
        for i in range(amount_of_playing_squares):
            next_coord = self.get_next_square(start_coord)
            start_coord = next_coord
            result.append(next_coord)
        return result

    # # TODO add this to coord_system
    def get_next_step(self, index, amount):
        next_index = index + amount
        return self.path[next_index - len(self.path)] if next_index > len(self.path) - 1 else self.path[next_index]

    # TODO add this to game_mechanics
    @staticmethod
    def get_home(coords: Coords, amount):
        x, y = coords
        if y > 0 or x > 0:
            return coords.change_higher(-amount)
        else:
            return coords.change_higher(amount)

    # TODO add this to game_mechanics
    @staticmethod
    def get_quadrant(coords: Coords):
        res = [coord > 0 for coord in coords]
        quadrants = {1: [False, True], 2: [False, False], 3: [True, False], 4: [True, True]}

        for k, v in quadrants.items():
            if v == res:
                return k

    # TODO add this to game_mechanics
    @property
    def mid(self):
        return [i for i in range(2, self.board_size // 2)]

    # TODO add this to game_mechanics
    def get_direction(self, coords: Coords):
        coords_abs = abs(coords)
        x, y = coords
        x_abs, y_abs = coords_abs

        quadrant = self.get_quadrant(coords)
        movements = {1: [1, 1], 2: [-1, 1], 3: [-1, -1], 4: [1, -1]}

        if 0 in coords:
            return [x == 0, y == 0]

        if any(abs_coords in self.mid for abs_coords in coords_abs):
            return [x_abs > 1, y_abs > 1]

        if self.board_size // 2 in coords_abs:
            if 0 in [x + movements[quadrant][0], y + movements[quadrant][1]]:
                return [x_abs < y_abs, y_abs < x_abs]
            else:
                return [x_abs > y_abs, y_abs > x_abs]

        return [x == movements[quadrant][0], y == movements[quadrant][1]]

    # TODO add this to game_mechanics
    def get_next_square(self, coords: Coords):
        edge_cases = {(0, self.board_size // 2): [1, 0],
                      (-self.board_size // 2, 0): [0, 1],
                      (0, -self.board_size // 2): [-1, 0],
                      (self.board_size // 2, 0): [0, -1]}

        if (tpl := tuple(coords.value)) in edge_cases:
            return coords + Coords(value=edge_cases[tpl])

        direction = self.get_direction(coords)
        quad = self.get_quadrant(coords)
        movements = {1: Coords(1, 1), 2: Coords(-1, 1), 3: Coords(-1, -1), 4: Coords(1, -1)}

        return coords.change_one_direction(movements[quad], direction)
