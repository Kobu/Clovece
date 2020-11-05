import random
import copy
import coord_system
import figurine
import game_board
import player
from game_math import *


# TODO pick a figurine u want to move = extract a method

# TODO instead of passing player to check top square, pass top square instead

# TODO print players in their colour
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

    # NOTE ignore for now, belongs here
    def pick_figurine(self, player):
        pick_board = copy.deepcopy(self.board.board)
        dictionary = {}
        for index, figurine in enumerate(player.figurines):
            if figurine.position is None:
                continue
            else:
                x, y = translate_to_normal(figurine.position, self.board.size // 2)
                pick_board[x][y] = '\033[1m' + '\033[94m' + game_board.FIGURINE_LETTERS[index] + '\033[94m' + '\033[0m'
                dictionary[game_board.FIGURINE_LETTERS[index]] = figurine

        print("".join(["".join(row) + "\n" for row in pick_board]))
        result = input()

        try:
            res = dictionary[result]
            return res
        except Exception:
            print("Figurine cant be picked")

    # NOTE main method that gets called
    # belongs here, prone to changes
    def turn(self, top_square, fig: figurine.Figurine, dice):
        if not dice:  # remove this, testing purposes only
            dice = self.mechanics.throw()
        coords = fig.position

        calculated_moves = self.mechanics.calculate_moves(dice, top_square, coords)
        last_move = calculated_moves[len(calculated_moves) - 1]

        if not self.is_move_sequence_possible(calculated_moves, fig):
            return

        for move in calculated_moves:
            if self.is_occupied(move):
                self.handle_figurines_meeting(move, fig)

        self.board.update_player_pos(fig.name, last_move, fig.position)
        fig.set_pos(last_move)
        fig.home = self.mechanics.is_fig_home(last_move)

    # DONE, belongs here
    # remove enemy figurines that are stepped on
    def handle_figurines_meeting(self, coords, fig):
        another_figurine = self.get_fig_from_coords(coords)
        if another_figurine.owner != fig.owner:
            self.board.update_player_pos(another_figurine.name, None, another_figurine.position)
            another_figurine.knockout_figurine()

    def is_move_sequence_possible(self, calculated_moves, fig):
        last_move = calculated_moves[len(calculated_moves) - 1]
        return False if None in calculated_moves else self.can_step_on_coords(last_move, fig)

    # DONE, belongs here
    def can_step_on_coords(self, coords, fig: figurine.Figurine):
        if self.is_occupied(coords):
            return self.get_fig_from_coords(coords).owner != fig.owner
        else:
            return True

    # DONE, belongs here
    def is_occupied(self, coords):
        for player in self.players:
            for figurine in player.figurines:
                if figurine.position == coords:
                    return True
        return False

    # DONE, belongs here
    def get_fig_from_coords(self, coords):
        for player in self.players:
            for figurine in player.figurines:
                if figurine.position == coords:
                    return figurine
        return None
