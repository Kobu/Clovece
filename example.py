import game
import game_board
import player

board = game_board.Board(9, "○", "○", " ", " ")

player1 = player.Player("kobu")
player2 = player.Player("slendy")

game = game.Clovece(board, [player1, player2])

game.main()
