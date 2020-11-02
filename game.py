import random

import figurine
import game_board
import player

# TODO make an exception system in self.is_move_possible, try-except in self.turn

# TODO move inside home square

# TODO pick a figurine u want to move
class Clovece:
    def __init__(self, board: game_board.Board, players):
        self.board = board

        self.players = players
        self.prepare_game()

        self.square = [-(self.board.size // 2), 1]
        self.path = self.calculate_path()

    def prepare_game(self):
        for index, player in enumerate(self.players):
            player.start_square = self.board.start_squares[index]
            player.top_square = self.board.top[index]

            player.color = game_board.COLORS[index]
            player.letter = game_board.LETTERS[index]

    def calculate_path(self):
        result = []
        # TODO clean this, remove self.square
        for i in range(4 * self.board.size - 4):
            next_square = self.get_next_square(self.square)
            self.square = next_square
            result.append(next_square)
        return result




    def is_occupied(self, coords):
        for player in self.players:
            for figurine in player.figurines:
                if figurine.position == coords:
                    return figurine
        return None

    @staticmethod
    def throw():
        a = []
        while(True):
            dice = random.randint(1,6)
            a.append(dice)
            if dice != 6:
                break
        return a


    # TODO will call is_move_possible
    def turn(self, player: player.Player):
        dice = self.throw()
        fig = player.pick_figurine()

        # for number in dice:
            # try move possible ?
                # if possible - return coords
                # tepm_coords = coords
            # except Exception as e:
                # print(e)

    def can_initialize_figurine(self, dice, fig: figurine.Figurine, player: player.Player):
        pass

    # TODO code needs to be restructured to allow throwing a 6
    # TODO maybe an upper method that contains the self.throw() method
    # TODO return type = bool ?, [next_pos, previous pos] / None(error message)?
    # if error_message then print the message and return
    # else
    def is_move_possible(self, dice, fig: figurine.Figurine, player: player.Player):
        previous_pos = fig.position

        # a player can pick:
            # a figurine thats already home:
                # can move DICE amount of squares ?
                    # true -> move it
                    # false -> pick another figurine
            # a figurine on playing square:
                # can move DICE amount of squares ?
                    # true - >
                        # is there another figurine ?
                            # true ->
                                # is it your figurine ?
                                    # true -> pick another figurine
                                    # false -> knock out the other player and move here
                            # false ->
                                # move here
                    # false ->
                        # pick another figurine
        # a figurine not initialized
            # can it be initialized ? (== u dont have ur own figurine standing on ur start square)

        # TODO extract a method here
        # if not player.has_figurine_out():
        #     print("checking if has figurines out")
        #     if dice == 6:
        #         print("threw 6")
        #         fig.initialize_figurine(player.start_square)
        #         self.board.update_player_pos(player.letter, player.start_square)
        #         return
        #     else:
        #         print("no figurines out and didn't throw 6")
        #         return

        if fig.home:
            print("already home")
            # TODO can be removed ?
            return [fig.position, None]
            # self.board.update_player_pos(fig.name, fig.position)
            # return

        coords = self.calculate_move_sequence(dice, player, fig)

        # TODO extract a method here
        if fig2 := self.is_occupied(coords):
            print("is occupied")
            if fig2 == fig:
                return
            if fig2.owner == fig.owner and dice !=6:
                print("cant go here, u got a figurine there")
                return
            else:
                # TODO delete the other player and update the board,
                fig2.remove_from_board()
                print(fig2.position)
                self.board.update_player_pos(fig.name, coords, fig2.position)
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
            print("successfully gone to home")
            fig.in_home()
            return self.get_home(coords, amount)

    def calculate_move_sequence(self, dice,  play: player.Player, fig: figurine.Figurine):
        index = self.path.index(fig.position)
        print(f"{play.color} threw: {dice}")

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
            else:
                return next_square
        # return next_square

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

player1 = player.Player("kobu")

player2 = player.Player( "max")

game = Clovece(board1, [player1, player2])
game.board.print_board()

#
print(game.throw())
# for i in range(20):
#     game.is_move_possible(player1.figurines[0], player1)
#
#     game.board.print_board()
#     print("_________________")
