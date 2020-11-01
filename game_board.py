class Board:
    def __init__(self, size, playing_square, home_square, middle_square, empty_square):
        self.size = size
        self.amnt_of_home_squares = self.size // 2 - 1

        self.empty_square = empty_square
        self.playing_square = playing_square
        self.home_square = home_square
        self.middle_square = middle_square

        self.start_squares = [[-self.size//2, 1], [1, self.size//2], [self.size//2, -1], [1, self.size//2]]
        self.top = [[0, self.size // 2], [-self.size // 2, 0], [0, -self.size // 2],[self.size // 2, 0]]

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

    def translate_to_negative(self, coords):
        return [coords[0] - self.size // 2, coords[1] - self.size // 2]

    def translate_to_normal(self, coords):
        return [coords[0] + self.size // 2, coords[1] + self.size // 2]

    def delete_previous_pos(self, previous_pos):
        x,y = self.translate_to_normal(previous_pos)
        self.board[x][y] = self.playing_square

    def update_player_pos(self, fig_name, coords: list, previous_pos=None):
        x, y = self.translate_to_normal(coords)

        if previous_pos:
            self.delete_previous_pos(previous_pos)

        self.board[x][y] = fig_name

    def print_board(self):
        print("".join(["".join(row) + "\n" for row in self.board]))
