import random

import coord_system
import figurine
import game_board
import player
from game_mechanics import *


# TODO make an exception system in self.is_move_possible, try-except in self.turn
# maybe not ?
# TODO implement a self.set_pos(figurine) method that is wrapped around by board.update_player_pos_method, also may set the fig.home flag ?

# TODO pick a figurine u want to move = exctract a method
class Clovece:
    def __init__(self, board: game_board.Board, players):
        self.board = board

        self.players = players
        self.prepare_game()

        self.mechanics = GameMechanics(self.board.size)

    def prepare_game(self):
        for index, player in enumerate(self.players):
            player.start_square = self.board.start_squares[index]
            player.top_square = self.board.top[index]

            player.color = game_board.COLORS[index]
            player.letter = game_board.LETTERS[index]
            player.create_figurines()

    # DONE
    @staticmethod
    def throw():
        a = []
        while True:
            dice = random.randint(1, 6)
            a.append(dice)
            if dice != 6:
                break
        return a
        # return [6, 6, 1]

    def calculate_moves(self, dice, player, coords):
        return [self.calculate_next_square(number, player, coords) for number in dice]

    def is_move_sequence_possible(self, calculated_moves, fig):
        last_move = calculated_moves[len(calculated_moves)-1]
        # TODO AND NOT NONE IN caulcated_moves
        return self.is_coord_available(last_move, fig)

    def turn(self, player: player.Player):
        dice = self.throw()
        fig = player.figurines[0]
        coords = fig.position

        # TODO there MUST be a fig.home check here, before calculating moves

        calculated_moves = self.calculate_moves(dice, player, coords)

        if self.is_move_sequence_possible(calculated_moves, fig):
            for index, move in enumerate(calculated_moves):  # TODO extract method here

                if index == 0:
                    self.do_move(move, fig, fig.position)
                else:
                    self.do_move(move, fig, calculated_moves[index - 1])

                if index == len(calculated_moves) - 1:
                    fig.set_pos(move)

    # REFACTOR could add this to Figurine class
    def can_step_on_coords(self, coords, fig: figurine.Figurine):
        if self.is_occupied(coords):
            return self.get_fig_from_coords(coords).owner != fig.owner
        else:
            return True

    # DONE
    def is_occupied(self, coords):
        for player in self.players:
            for figurine in player.figurines:
                if figurine.position == coords:
                    return True
        return False

    # DONE
    def get_fig_from_coords(self, coords):
        for player in self.players:
            for figurine in player.figurines:
                if figurine.position == coords:
                    return figurine
        return None

    # TODO completly remake this
    def do_move(self, coords, fig: figurine.Figurine, previous_coords):
        pass

    # TEST needed
    # REFACTOR maybe add this to the figurine class, remove coords, use fig.pos instead
    # called when standing inside home OR at the top square
    @staticmethod
    def can_move_in_home(coords, dice):
        abs_x, abs_y = coord_system.make_abs(coords)

        return max(abs_x, abs_y) - dice > 0

    def is_on_top_square(self, coords, player, dice):

    def calculate_next_square(self, dice, play: player.Player, coords):
        print(f"{play.color} threw: {dice}")

        # REFACTOR could extract a is_on_top_square method from this
        if coords == play.top_square:
            print("standing on home")
            if self.can_move_in_home(coords, dice):
                print("can move in home")
                return self.mechanics.get_home(coords, dice)
            else:
                #  NOTE will return None to represent an impossible move
                return None
        index = self.mechanics.path.index(coords)
        next_square = None

        # TODO maybe simplify this ?
        for i in range(1, dice + 1):
            next_square = self.mechanics.get_next_step(index, i)

            # will aim to home
            if next_square == play.top_square and dice != i:
                # check if the move is possible
                if self.can_move_in_home(next_square, dice-i):
                    return self.mechanics.get_home(next_square, dice - i)

        return next_square



board1 = game_board.Board(9, "O", "X", " ", ".")

player1 = player.Player("kobu")

player2 = player.Player("max")

game = Clovece(board1, [player1, player2])
game.board.print_board()

player1.figurines[0].set_pos([4, 0])

for i in range(5):
    game.turn(player1)
    game.board.print_board_raw()
    game.board.print_board()
