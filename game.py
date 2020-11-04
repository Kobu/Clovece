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

    # TODO change to is_occupied -> bool and get_fig_on_coords -> figurine
    def is_occupied(self, coords):
        for player in self.players:
            for figurine in player.figurines:
                if figurine.position == coords:
                    return figurine
        return False

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

    def calculate_moves(self, dice, player, coords, fig):
        return [self.calculate_next_square(number, player, coords, fig) for number in dice]

    def is_move_sequence_possible(self, calculated_moves, fig):
        last_move = calculated_moves[len(calculated_moves)-1]
        return self.is_coord_available(last_move, fig)

    def turn(self, player: player.Player):
        dice = self.throw()
        fig = player.figurines[0]
        coords = fig.position

        # TODO there MUST be a fig.home check here, before calculating moves
        # if home -> check cam_move_in_home am=nd return

        # calculated_moves = []  # TODO extract method here
        # for number in dice:
        #     coords = self.calculate_next_square(number, player, coords, fig)
        #     calculated_moves.append(coords)
        calculated_moves = self.calculate_moves(dice, player, coords, fig)

        # # TODO extract method here
        # for move in calculated_moves:
        #     possible_moves.append(self.is_coord_available(move, fig))

        # if possible_moves[len(possible_moves) - 1]:  # TODO extract a simple method here
        if self.is_move_sequence_possible(calculated_moves, fig):
            for index, move in enumerate(calculated_moves):  # TODO extract method here

                if index == 0:
                    self.do_move(move, fig, fig.position)
                else:
                    self.do_move(move, fig, calculated_moves[index - 1])

                if index == len(calculated_moves) - 1:
                    fig.set_pos(move)

    # TODO maybe add an decorator that would update the board ?
    # TODO move line 76 here ?
    def do_move(self, coords, fig: figurine.Figurine, previous_coords):
        if another_figurine := self.is_occupied(coords):
            if another_figurine.owner != fig.owner:
                self.board.update_player_pos(another_figurine.name, None, another_figurine.position)
                another_figurine.knockout_figurine()
        self.board.update_player_pos("B", coords, previous_coords)

    # if error_message then print the message and return
    # else
    def is_coord_available(self, coords, fig: figurine.Figurine):
        if not coords:
            return False

        # TODO something smells here
        if another_figurine := self.is_occupied(coords):
            return another_figurine.owner != fig.owner
        else:
            return True

    # called when standing iside home
    def can_move_in_home(self, coords, dice):
        abs_x, abs_y = coord_system.make_abs(coords)

        if max(abs_x, abs_y) - dice > 0:
            return self.mechanics.get_home(coords, dice)
        else:
            # raise exception here
            # cant move, pick another figurine or halt
            return False

    def calculate_next_square(self, dice, play: player.Player, coords, fig):
        # TODO replace with a if is.home check

        print(f"{play.color} threw: {dice}")
        try:
            index = self.mechanics.path.index(coords)
        except ValueError:
            return self.can_move_in_home(coords, dice)

        # TODO can be put outside of the for loop block ?
        if coords == play.top_square:
            print("standing on home")
            return self.go_to_home(fig, coords, dice)

        next_square = None

        # TODO maybe simplify this ?
        for i in range(1, dice + 1):
            next_square = self.mechanics.get_next_step(index, i)

            # # TODO can be put outside of the for loop block ?
            # if coords == play.top_square:
            #     print("standing on home")
            #     return self.go_to_home(fig, coords, dice)
            # if (next_square := self.path[next_index]) == play.top_square:
            # next_square = self.mechanics.path[next_index]
            # TODO Simplify this
            if next_square == play.top_square:
                if i == dice:
                    print("stopped at home")
                    return next_square
                else:
                    print("to home")
                    return self.go_to_home(fig, next_square, dice - i)
            else:
                print("clear path")
        return next_square

    # called when standing on top square
    # TODO restructure to return a bool/None if amount > self.board.amnt_of_home_squares, remove fig as paraneter
    # TODO this MUST be changed, fig.in_home needs to be removed
    def go_to_home(self, fig: figurine.Figurine, coords, amount):
        if amount > self.board.amnt_of_home_squares:
            print("number too high")
            return fig.position
        else:
            print("successfully gone to home")
            fig.in_home()
            return self.mechanics.get_home(coords, amount)


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
