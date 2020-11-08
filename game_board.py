from termcolor import colored

import coord_system

COLORS = ["blue", "green", "yellow", "red"]
LETTERS = ["B", "G", "Y", "R"]
FIGURINE_LETTERS = ["1", "2", "3", "4"]  # TODO what if theres more than 4 figruines


class Board:
    def __init__(self, size, playing_square, home_square, middle_square, empty_square):
        self.size = size
        self.amnt_of_home_squares = self.size // 2 - 1

        self.empty_square = empty_square
        self.playing_square = playing_square
        self.home_square = home_square
        self.middle_square = middle_square

        self.top = [[-(self.size // 2), 0], [0, self.size // 2], [self.size // 2, 0],
                    [0, -(self.size // 2)]]
        self.start_squares = [[-(self.size // 2), 1], [1, self.size // 2], [self.size // 2, -1],
                              [1, self.size // 2]]

        self.board = self.create_board()

    def create_board(self):
        board = [[self.empty_square] * self.size for i in range(self.size)]
        for y in range(self.size):
            for x in range(self.size):

                if abs(x - self.size // 2) <= 1 or abs(y - self.size // 2) <= 1:
                    board[x][y] = self.playing_square

                if x not in [0, self.size - 1]:
                    if x < self.size // 2 and y == self.size // 2:
                        board[x][y] = colored(self.home_square, "blue")
                    elif x > self.size // 2 and y == self.size // 2:
                        board[x][y] = colored(self.home_square, "red")

                if y not in [0, self.size - 1]:
                    if y > self.size // 2 and x == self.size // 2:
                        board[x][y] = colored(self.home_square, "green")
                    elif y < self.size // 2 and x == self.size // 2:
                        board[x][y] = colored(self.home_square, "yellow")

                if [x, y] == [self.size // 2, self.size // 2]:
                    board[x][y] = self.middle_square

        return board

    def delete_previous_pos(self, previous_pos):
        x, y = coord_system.translate_to_normal(previous_pos, self.size // 2)
        self.board[x][y] = self.playing_square

    def update_player_pos(self, fig_name, new_coords, previous_coords=None):
        # TODO can be simplified
        # TODO clean this mess

        if new_coords is None:
            self.delete_previous_pos(previous_coords)
            return
        else:
            x, y = coord_system.translate_to_normal(new_coords, self.size // 2)
            self.board[x][y] = fig_name

        if previous_coords:
            self.delete_previous_pos(previous_coords)

    def print_board(self):
        print("".join(["".join(row) + "\n" for row in self.board]))

    def print_board_raw(self):
        for row in self.board:
            print(row)

    # def pick_figurine(self, board, coords):
    #     for coord in coords:
