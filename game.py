import game_board
import figurine
import player
import random


class Clovece:
    def __init__(self, board: game_board.Board, players):
        self.board = board

        self.players = players
        self.set_top_square()
        self.set_start_squares()
        # self.set_figurines()
        # self.fig2 = fig2

        self.square = [-(self.board.size // 2), 1]
        self.path = self.calculate_path()

    def calculate_path(self):
        result = []
        for i in range(4 * self.board.size - 4):
            next_square = self.get_next_square(self.square)
            self.square = next_square
            result.append(next_square)
        return result

    # def set_figurines(self):
    #     for player in self.players:
    #         for figurine in player.figurines:
    #             # TODO set eachs player unique letter
    #             self.board.update_player_pos(figurine.name, figurine.position)

    def set_start_squares(self):
        for index, player in enumerate(self.players):
            player.set_start_square(self.board.start_squares[index])

    def set_top_square(self):
        for index, player in enumerate(self.players):
            player.set_top_square(self.board.top[index])

    def is_occupied(self, coords):
        for player in self.players:
            for figurine in player.figurines:
                if figurine.position == coords:
                    return figurine
        return None

    @staticmethod
    def throw():
        return random.randint(1, 6)

    def turn(self, fig: figurine.Figurine, play: player.Player):
        previous_pos = fig.position

        if fig.home:
            print("already home")
            self.board.update_player_pos(fig.name, fig.position)
            return

        coords = self.calculate_move_sequence(play, fig)

        if fig2 := self.is_occupied(coords):
            if fig2.owner == fig.owner:
                print("cant go here, u got a figurine there")
                return
            if fig2 == fig:
                return
            else:
                # TODO delete the other player = update the board,
                fig2.remove_from_board()
                self.board.update_player_pos(fig.name, coords, fig2.pos)
        fig.set_pos(coords)
        self.board.update_player_pos(fig.name, coords, previous_pos)

    def get_next_index(self, index, amount):
        return index + amount - len(self.path) if index + amount > len(self.path) - 1 else index + amount

    # called when standing on top square
    def go_to_home(self, fig: figurine.Figurine, coords, amount):
        if amount > self.board.amnt_of_home_squares:
            print("number too high")
            return fig.position
        else:
            print("succesfuly gone to ohome")
            fig.in_home()
            return self.get_home(coords, amount)

    def calculate_move_sequence(self, play: player.Player, fig: figurine.Figurine):
        dice = self.throw()
        index = self.path.index(fig.position)
        print(dice)

        for i in range(1, dice + 1):
            next_index = self.get_next_index(index, i)
            if fig.position == play.top_square:
                # go to home
                print("standing on home")
                return self.go_to_home(fig, fig.position, dice)
            if (next_square := self.path[next_index]) == play.top_square:
                # go to home
                if i == dice:
                    print("stopped at home")
                    return next_square
                else:
                    print("to home")
                    return self.go_to_home(fig, next_square, dice - i)
        return next_square

    @staticmethod
    def get_home(coords, amnt):
        x, y = coords
        if abs(x) > abs(y):
            return [x - amnt, y] if x > 0 else [x + amnt, y]
        else:
            return [x, y - amnt] if y > 0 else [x, y + amnt]

    @staticmethod
    def get_quadrant(coords):
        res = [coord > 0 for coord in coords]
        quadrants = {1: [False, True], 2: [False, False], 3: [True, False], 4: [True, True]}

        for k, v in quadrants.items():
            if v == res:
                return k

    @property
    def mid(self):
        return [i for i in range(2, self.board.size // 2)]

    def get_direction(self, coords):
        coords_abs = [abs(coords[0]), abs(coords[1])]
        x, y = coords
        x_abs, y_abs = coords_abs

        quadrant = self.get_quadrant(coords)
        movements = {1: [1, 1], 2: [-1, 1], 3: [-1, -1], 4: [1, -1]}

        if 0 in coords:
            return [x == 0, y == 0]

        if any(coord in self.mid for coord in coords_abs):
            return [x_abs > 1, y_abs > 1]

        if self.board.size // 2 in coords_abs:
            if 0 in [x + movements[quadrant][0], y + movements[quadrant][1]]:
                return [x_abs < y_abs, y_abs < x_abs]
            else:
                return [x_abs > y_abs, y_abs > x_abs]

        return [x == movements[quadrant][0], y == movements[quadrant][1]]

    def get_next_square(self, coords):
        edge_cases = {(0, self.board.size // 2): [1, 0],
                      (-self.board.size // 2, 0): [0, 1],
                      (0, -self.board.size // 2): [-1, 0],
                      (self.board.size // 2, 0): [0, -1]}

        if (tpl := tuple(coords)) in edge_cases:
            return self.sum_coords(coords, edge_cases[tpl])

        direction = self.get_direction(coords)
        quad = self.get_quadrant(coords)
        movements = {1: [1, 1], 2: [-1, 1], 3: [-1, -1], 4: [1, -1]}

        return self.sum_coords(coords, movements[quad], direction)

    @staticmethod
    def sum_coords(coords1, coords2, one_directional=None):
        if one_directional:
            if one_directional[0]:
                return [coords1[0] + coords2[0], coords1[1]]
            else:
                return [coords1[0], coords1[1] + coords2[1]]
        else:
            return [coords1[0] + coords2[0], coords1[1] + coords2[1]]


board1 = game_board.Board(9, "O", "X", " ", ".")

figurka1 = figurine.Figurine("kobu", [-1, 3], "P")
player1 = player.Player("blue", "kobu", [figurka1])

figurka2 = figurine.Figurine("max", [-1, 3], "B")
player2 = player.Player("green", "max", [figurka2])

game = Clovece(board1, [player1, player2])

# game.board.print_board()
for player in game.players:
    print(player.top_square, player.start_square)