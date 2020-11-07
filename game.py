import copy

from termcolor import colored

import figurine
import game_board
import player
from game_math import *  # weird


# TODO print players in their colour

# TODO get permutations when going from home

# TODO create a turn method with infinite while loop (until all but one player have all their figs in home)
# will get next player, let him choose a figurine and call handle movement
# handle when incorrect figurine is chosen - prompt the player to choose again
# handle when player has no figurines out
# throwing 6 - HAVE to take out another figurine
# not throwing 6 - continue
# get multiset permutations
# will calculate calculated_moves - loop over every


# TODO the main method will consist of two while loops, one that represents the game itself, one that will represent players turn

# TODO make a successfully_chose_figurine method and loop it infinitely until it equals true


class Clovece:
    def __init__(self, board: game_board.Board, players: list):
        self.board = board
        self.players = players

        self.prepare_game()

        self.mechanics = GameMechanics(self.board.size)

    def prepare_game(self):
        for index, player in enumerate(self.players):
            player.start_square = self.board.start_squares[index]
            player.top_square = self.board.top[index]

            player.color = game_board.COLORS[index]
            player.fig_symbol = colored("●", player.color)
            player.figurines = player.create_figurines(self.board.amnt_of_home_squares)

    def next_player(self, player):
        next_player = self.players.index(player) + 1
        return self.players[next_player - len(self.players)] if next_player > len(self.players) - 1 else self.players[
            next_player]

    # NOTE ignore for now, belongs here
    def pick_figurine(self, player, moves):
        pick_board = copy.deepcopy(self.board.board)
        dictionary = {}
        active_figurines = player.get_active_figurines()

        while True:
            for index, figurine in enumerate(active_figurines):
                if moves[index] is True:
                    x, y = translate_to_normal(figurine.position, self.board.size // 2)

                    pick_board[x][y] = '\033[1m' + colored(game_board.FIGURINE_LETTERS[index], player.color) + '\033[0m'
                    dictionary[game_board.FIGURINE_LETTERS[index]] = figurine
                else:
                    continue

            print("".join(["".join(row) + "\n" for row in pick_board]))  # TODO extract a method here
            result = input()

            try:
                res = dictionary[result]
                return res
            except AttributeError:
                print("Figurine cant be picked")
            except KeyError:
                print("cant")

    def has_any_possible_moves(self, dice, player):
        active_figurines = player.get_active_figurines()

        return [self.is_move_sequence_possible(dice, player.top_square, fig) for fig in active_figurines]

    def is_game_ended(self):
        has_ended = [player.has_finished() for player in self.players]
        return has_ended.count(True) == len(self.players) - 1

    def must_draw_from_home(self, dice, player: player.Player):
        if len(player.get_active_figurines()) == self.board.amnt_of_home_squares:
            return False

        # if not player.has_figurine_out():
        #     return True

        if 6 not in dice:
            return False

        if self.is_occupied(player.start_square):  # TODO move to can_draw
            another_fig = self.get_fig_from_coords(player.start_square)
            print("here")
            return another_fig.owner != player.name
        else:
            return True

    def can_draw_from_home(self, player, dice):
        changed_dice = copy.deepcopy(dice)
        changed_dice.remove(6)
        fig = player.draw_fig_from_home()

        if not self.can_step_on_coords(player.start_square, fig):
            print("cant step on coords")
            return False

        return self.is_move_sequence_possible(changed_dice, player.top_square, fig, player.start_square)

    def play_game(self):
        player = self.players[0]

        while True:

            dice = self.mechanics.throw()
            # dice = [6, 1]

            print(f"{player.name} threw {dice}")

            self.handle_players_turn(dice, player)
            print("________________________")

            if self.is_game_ended():
                print(f"game has ended, {player.name} has won!")
                self.board.print_board()
                break

            player = self.next_player(player)

    def handle_players_turn(self, dice, player):
        # while True:

        if self.must_draw_from_home(dice, player) and self.can_draw_from_home(player, dice):
            self.handle_drawing_from_home(dice, player)
            self.board.print_board()
            return
            # break

        moves = self.has_any_possible_moves(dice, player)
        if not any(moves):
            print("no possible moves")
            self.board.print_board()
            return
            # break

        fig = self.pick_figurine(player, moves)

        move_order = self.mechanics.get_move_order(dice)
        move = self.mechanics.calculate_moves(move_order, player.top_square, fig.position)
        self.handle_movement(fig, move)

        # break

    def handle_drawing_from_home(self, dice, player):
        fig = player.draw_fig_from_home()

        changed_dice = copy.deepcopy(dice)
        changed_dice.remove(6)

        calculated_moves = self.mechanics.get_path_from_home(player.start_square, player.top_square, changed_dice)

        self.handle_movement(fig, calculated_moves)

    # belongs here, prone to changes
    def handle_movement(self, fig: figurine.Figurine, calculated_moves):
        last_move = calculated_moves[len(calculated_moves) - 1]

        for move in calculated_moves:
            if self.is_occupied(move):
                self.handle_figurines_meeting(move, fig)

        self.update_figurine(fig, last_move)

    def update_figurine(self, fig, last_move):
        self.board.update_player_pos(fig.name, last_move, fig.position)
        fig.set_pos(last_move)
        fig.home = self.mechanics.is_fig_home(last_move)

    # DONE, belongs here
    def handle_figurines_meeting(self, coords, fig):
        another_figurine = self.get_fig_from_coords(coords)

        if another_figurine.owner != fig.owner:
            self.board.update_player_pos(another_figurine.name, None, another_figurine.position)
            print(f"{fig.name} knocked out {another_figurine.name} at {coords}")
            another_figurine.knockout_figurine()

    def is_move_sequence_possible(self, dice, top_square, fig, start_square=None):
        # if fig.position is None:
        #     return False # this causes bugs
        coords = start_square if start_square else fig.position

        calculated_moves = self.mechanics.calculate_moves(dice, top_square, coords)
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
