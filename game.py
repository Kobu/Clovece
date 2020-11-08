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
        next_player_index = self.players.index(player) + 1
        next_player = self.players[next_player_index % len(self.players)]

        return next_player
        # return self.players[next_player - len(self.players)] if next_player > len(self.players) - 1 else self.players[
        #     next_player]

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
            result = input("Pick figurine to move with\n")

            try:
                res = dictionary[result]
                return res
            except AttributeError:
                print("Figurine cant be picked")
            except KeyError:
                print(f"Figurine '{result}' either doesnt exist or cant be moved with.")

    def get_possible_moves(self, dice, player):
        active_figurines = player.get_active_figurines()

        return [self.is_move_sequence_possible(dice, fig) for fig in active_figurines]

    def is_game_ended(self):
        has_ended = [player.has_finished() for player in self.players]
        return has_ended.count(True) == len(self.players) - 1

    def must_draw_from_home(self, dice, player: player.Player):
        if len(player.get_active_figurines()) == self.board.amnt_of_home_squares:
            return False

        if 6 not in dice:
            return False

        if self.is_occupied(player.start_square):
            another_fig = self.get_fig_from_coords(player.start_square)
            return another_fig.owner != player.name
        else:
            return True

    # REFACTOR maybe add can_step_on_coords to fig class ?
    def can_draw_from_home(self, player, dice):
        changed_dice = copy.deepcopy(dice)
        changed_dice.remove(6)

        fig = player.draw_fig_from_home()

        if not self.can_step_on_coords(fig.start_square, fig):
            return False

        return self.is_move_sequence_possible(changed_dice, fig, fig.start_square)

    def main(self):
        player = self.players[0]

        while True:
            if player.has_figurine_out():
                print(player.has_figurine_out())
                dice = self.mechanics.throw()
                print(f"{player.name} threw {dice}")
            else:
                for _ in range(3):
                    dice = self.mechanics.throw()
                    if 6 in dice:
                        print(f"{player.name} threw {dice}")
                        break
                    print(f"{player.name} didnt manage to throw a 6")

            # dice = [6,1]

            # print(f"{player.name} threw {dice}")

            self.handle_players_turn(dice, player)
            print("________________________")

            if self.is_game_ended():
                print(f"game has ended, {player.name} has won!")
                self.board.print_board()
                break

            player = self.next_player(player)

    def handle_players_turn(self, dice, player: player.Player):
        if self.must_draw_from_home(dice, player) and self.can_draw_from_home(player, dice):
            self.handle_drawing_from_home(dice, player)
            self.board.print_board()
            _ = input(f"{player.name} had to draw from home, press enter to continue \n")
            return

        possible_moves = self.get_possible_moves(dice, player)
        if not any(possible_moves):
            self.board.print_board()
            _ = input(f"{player.name} has no possible moves, press enter to continue \n")
            return
        else:
            fig = self.pick_figurine(player, possible_moves)

        move_order = self.mechanics.get_move_order(dice)
        move = self.mechanics.calculate_moves(move_order, fig.top_square, fig.position)
        self.handle_movement(fig, move)

    def handle_drawing_from_home(self, dice, player: player.Player):
        changed_dice = copy.deepcopy(dice)
        changed_dice.remove(6)

        fig = player.draw_fig_from_home()

        calculated_moves = self.mechanics.get_path_from_home(fig.start_square, fig.top_square, changed_dice)

        self.handle_movement(fig, calculated_moves)

    def handle_movement(self, fig: figurine.Figurine, calculated_moves):
        last_move = calculated_moves[len(calculated_moves) - 1]

        for move in calculated_moves:
            if self.is_occupied(move):
                self.handle_figurines_meeting(move, fig)

        self.update_figurine(fig, last_move)

    def update_figurine(self, fig, next_move):
        self.board.update_player_pos(fig.name, next_move, fig.position)
        fig.set_pos(next_move)
        fig.home = self.mechanics.is_fig_home(next_move)

    # DONE, belongs here
    def handle_figurines_meeting(self, coords, fig):
        another_figurine = self.get_fig_from_coords(coords)

        if another_figurine.owner != fig.owner:
            self.board.update_player_pos(another_figurine.name, None, another_figurine.position)
            print(f"{fig.name} knocked out {another_figurine.name} at {coords}")
            another_figurine.knockout_figurine()

    def is_move_sequence_possible(self, dice, fig: figurine.Figurine, from_home=None):
        coords = fig.start_square if from_home else fig.position

        calculated_moves = self.mechanics.calculate_moves(dice, fig.top_square, coords)
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
