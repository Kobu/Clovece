import random

import coord_system
import figurine
import game_board
import player
from game_mechanics import *


# TODO make an exception system in self.is_move_possible, try-except in self.turn
# maybe not ?

# TODO pick a figurine u want to move = exctract a method

# TODO instead of passing player to check top square, pass top swuare instead
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

    # DONE
    def calculate_moves(self, dice, player, coords):
        return [self.calculate_next_square(number, player, coords) for number in dice]

    def is_move_sequence_possible(self, calculated_moves, fig):
        last_move = calculated_moves[len(calculated_moves)-1]
        return False if None in calculated_moves else self.can_step_on_coords(last_move, fig)

    def turn(self, player: player.Player):
        dice = self.throw()
        fig = player.figurines[0] # pick figurines
        coords = fig.position

        # TODO there MUST be a fig.home check here, before calculating moves or in methods under

        calculated_moves = self.calculate_moves(dice, player, coords)
        last_move = calculated_moves[len(calculated_moves)-1]

        if self.is_move_sequence_possible(calculated_moves, fig):
            for index, move in enumerate(calculated_moves):  # refactor this, remove enumerate
                self.do_move()

            fig.set_pos(last_move)

            # dont forget to set the pos
        # TODO completly remake this

    # maybe an HANDLE_FIGURINE method that would be called if coord is occupied (in self.turn)
    # remove enemy figurines that are stepped on
    def do_move(self, coords, fig):
        another_figurine = self.get_fig_from_coords(coords)

        if another_figurine is None:
            return
        elif another_figurine.owner != fig.owner:
            another_figurine.set_pos(None)
        else:
            pass


    # REFACTOR could add this to Figurine class - maybe not because u need to check every figurine
    def can_step_on_coords(self, coords, fig: figurine.Figurine):
        if self.is_occupied(coords):
            return self.get_fig_from_coords(coords).owner != fig.owner
        else:
            return True

    # REFACTOR this could be deleted, use can_step_on_coords instead?
    # could be used when checking if start square is empty - that only needs to check one player -> add this to player class ?
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

    # TEST needed
    # REFACTOR maybe add this to the figurine class, remove coords, use fig.pos instead
    # called when standing inside home OR at the top square
    # NOTE does this check if amount_of_top_squares is higher than xxx ?
    @staticmethod
    def can_move_in_home(coords, dice):
        abs_x, abs_y = coord_system.make_abs(coords)

        return max(abs_x, abs_y) - dice > 0

    # NOTE this is merging can_move_in_home and go to home - smart
    def go_to_home(self, coords, dice):
        return self.mechanics.get_home(coords, dice) if self.can_move_in_home(coords, dice) else None

    # works
    def calculate_next_square(self, dice, play: player.Player, coords):
        print(f"{play.color} threw: {dice}")

        # REFACTOR could extract a is_on_top_square method from this - WRONG
        # REFACTOR keep the if statement and extract a method from rest
        if coords == play.top_square: # or fig.homr
            return self.go_to_home(coords, dice)

        index = self.mechanics.path.index(coords)
        next_square = None

        # TODO maybe simplify this ?
        for i in range(1, dice + 1):
            next_square = self.mechanics.get_next_step(index, i)

            # will aim to home
            if next_square == play.top_square and i != dice:
                return self.go_to_home(next_square, dice-i)

        return next_square
