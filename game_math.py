import random

from sympy.utilities.iterables import multiset_permutations

from coord_system import *


# TODO creating the path can be simplified by a simple for loop code block


class GameMechanics:
    def __init__(self, board_size):
        self.board_size = board_size

        self.path = self.get_path()

    ####################### PATH CALCULATIONS ###############################
    @property
    def mid(self):
        return [i for i in range(2, self.board_size // 2)]

    def get_next_step(self, index, amount):
        next_step_index = (index + amount)% len(self.path)
        next_step = self.path[next_step_index]

        return next_step
        # return self.path[next_index - len(self.path)] if next_index > len(self.path) - 1 else self.path[next_index]

    @staticmethod
    def get_quadrant(coords):
        res = [coord > 0 for coord in coords]
        quadrants = {1: [False, True], 2: [False, False], 3: [True, False], 4: [True, True]}

        for k, v in quadrants.items():
            if v == res:
                return k

    def get_direction(self, coords):
        coords_abs = make_abs(coords)

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

    def get_next_square(self, coords):

        edge_cases = {(0, self.board_size // 2): [1, 0],
                      (-self.board_size // 2, 0): [0, 1],
                      (0, -self.board_size // 2): [-1, 0],
                      (self.board_size // 2, 0): [0, -1]}

        key = tuple(coords)  # only to look up in the edge_cases table
        if key in edge_cases:
            return add(coords, edge_cases[key])

        direction = self.get_direction(coords)
        quadrant = self.get_quadrant(coords)
        movements = {1: [1, 1], 2: [-1, 1], 3: [-1, -1], 4: [1, -1]}

        return change_one_direction(coords, movements[quadrant], direction)

    def get_path(self):
        start_coord = [self.board_size // 2, 1]
        amount_of_playing_squares = 4 * self.board_size - 4

        result = []
        # TODO could be simplified be declaring next_coord outside of the loop an assigning it start_coord
        for i in range(amount_of_playing_squares):
            next_coord = self.get_next_square(start_coord)
            start_coord = next_coord
            result.append(next_coord)
        return result

    ################################ HOME PATH CALCULATIONS ###############################

    @staticmethod
    def get_home(coords, amount):
        x, y = coords
        if y > 0 or x > 0:
            return change_higher(coords, -amount)
        else:
            return change_higher(coords, amount)

    @staticmethod
    def can_move_in_home(coords, dice):
        abs_x, abs_y = make_abs(coords)

        return max(abs_x, abs_y) - dice > 0

    # NOTE this is disgusting, but it works
    def is_fig_home(self, coords):
        return coords not in self.path and coords is not None

    # NOTE returns None if the move is impossible
    def go_to_home(self, coords, dice):
        return self.get_home(coords, dice) if self.can_move_in_home(coords, dice) else None

    def get_path_from_home(self, start_square, top_square, dice):
        first_move = start_square
        calculated_moves = self.calculate_moves(dice, top_square, start_square)

        return [first_move, *calculated_moves]

    ################################ UNIVERSALLY USED CALCULATIONS ###############################

    # DONE
    # basically a do - while
    @staticmethod
    def throw():
        dice = []
        while True:
            number = random.randint(1, 6)
            dice.append(number)
            if number != 6:
                break
        return dice

    @staticmethod
    def get_dice_permutations(dice):
        return list(multiset_permutations(dice))

    def calculate_moves(self, dice, top_square, coords):
        next_coords = coords

        moves = []
        for number in dice:
            next_coords = self.calculate_next_square(number, top_square, next_coords)
            moves.append(next_coords)
            if next_coords is None:  # NONE represents an impossible move sequence, loop can be stopped because NONE is checked for later on
                break
        return moves

    def calculate_next_square(self, dice, top_square, coords):
        if coords == top_square:
            return self.go_to_home(coords, dice)

        if self.is_fig_home(coords):
            return self.go_to_home(coords, dice)

        index = self.path.index(coords)
        next_square = None

        for i in range(1, dice + 1):
            next_square = self.get_next_step(index, i)

            # will aim to home
            if next_square == top_square and i != dice:
                return self.go_to_home(next_square, dice - i)

        return next_square

    ################################ HELPER METHODS ################################

    def create_move_order_choice_prompt(self, dice):
        permutations = self.get_dice_permutations(dice)

        return {index: move for index, move in enumerate(permutations)}

    @staticmethod
    def handle_move_order_choice_prompt(move_dict):
        user_input = int(input())

        while True:
            try:
                return move_dict[user_input]
            except KeyError:  # keyerror ?
                print("invalid move")
                user_input = int(input())
            except ValueError:
                print("invalid move")
                user_input = int(input())

    def get_move_order(self, dice):
        if len(dice) > 1:
            move_order = self.create_move_order_choice_prompt(dice)
            print(f"possible moves: {move_order}")

            return self.handle_move_order_choice_prompt(move_order)
        else:
            return dice





