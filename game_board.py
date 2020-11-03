from coord_system import *

COLORS = ["Blue", "Green", "Yellow", "Red"]
LETTERS = ["B", "G", "Y", "R"]


class Board:
    def __init__(self, size, playing_square, home_square, middle_square, empty_square):
        self.size = size
        self.amnt_of_home_squares = self.size // 2 - 1

        self.empty_square = empty_square
        self.playing_square = playing_square
        self.home_square = home_square
        self.middle_square = middle_square

        self.top = [Coords(-(self.size // 2), 0), Coords(0, self.size // 2), Coords(self.size // 2, 0),
                    Coords(0, -(self.size // 2))]
        self.start_squares = [Coords(-(self.size // 2), 1), Coords(1, self.size // 2), Coords(self.size // 2, -1),
                              Coords(1, self.size // 2)]

        self.board = self.create_board()

    def create_board(self):
        board = [[self.empty_square] * self.size for i in range(self.size)]
        for y in range(self.size):
            for x in range(self.size):
                if abs(x - self.size // 2) <= 1 or abs(y - self.size // 2) <= 1:
                    board[x][y] = self.playing_square
                if (x - self.size // 2 == 0 and y != 0 and y != self.size - 1) or (
                        y - self.size // 2 == 0 and x != 0 and x != self.size - 1):
                    board[x][y] = self.home_square
                if [x, y] == [self.size // 2, self.size // 2]:
                    board[x][y] = self.middle_square

        return board

    def delete_previous_pos(self, previous_pos: Coords):
        x, y = previous_pos.translate_to_normal(self.size // 2)
        self.board[x][y] = self.playing_square

    def update_player_pos(self, fig_name, new_coords: Coords, previous_coords=None):
        # TODO can be simplified
        if new_coords is None:
            self.delete_previous_pos(previous_coords)
            return
        else:
            x, y = new_coords.translate_to_normal(self.size // 2)
            self.board[x][y] = fig_name

        if previous_coords:
            self.delete_previous_pos(previous_coords)

    def print_board(self):
        print("".join(["".join(row) + "\n" for row in self.board]))
