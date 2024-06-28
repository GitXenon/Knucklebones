import unittest
from unittest.mock import patch
from knucklebones import Board, Player, AIPlayer, Knucklebone


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_reset(self):
        self.board.grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.board.reset()
        self.assertEqual(
            self.board.grid,
            [[None, None, None], [None, None, None], [None, None, None]],
        )

    def test_update_column(self):
        self.assertTrue(self.board.update_column(1, 5))
        self.assertEqual(self.board.grid[0][0], 5)
        self.assertTrue(self.board.update_column(1, 3))
        self.assertEqual(self.board.grid[0][1], 3)
        self.assertTrue(self.board.update_column(1, 1))
        self.assertEqual(self.board.grid[0][2], 1)
        self.assertFalse(self.board.update_column(1, 6))

    def test_is_valid_move(self):
        self.assertTrue(self.board.is_valid_move(1))
        self.board.grid[0] = [1, 2, 3]
        self.assertFalse(self.board.is_valid_move(1))

    def test_column_score(self):
        self.board.grid = [[1, 1, 2], [3, 3, 3], [1, 2, None]]
        self.assertEqual(self.board.column_score(), [6, 27, 3])

    def test_score(self):
        self.board.grid = [[1, 1, 2], [3, 3, 3], [1, 2, None]]
        self.assertEqual(self.board.score(), 36)


class TestPlayer(unittest.TestCase):
    def test_player_initialization(self):
        player = Player("blue", "Alice")
        self.assertEqual(player.color, "blue")
        self.assertEqual(player.name, "Alice")
        self.assertIsInstance(player.board, Board)


class TestAIPlayer(unittest.TestCase):
    def setUp(self):
        self.ai_player = AIPlayer("red", "medium")

    def test_ai_player_initialization(self):
        self.assertEqual(self.ai_player.color, "red")
        self.assertEqual(self.ai_player.difficulty, "medium")
        self.assertIsInstance(self.ai_player.board, Board)

    @patch("random.choice")
    def test_choose_column_easy(self, mock_choice):
        self.ai_player.difficulty = "easy"
        mock_choice.return_value = 1
        self.assertEqual(self.ai_player.choose_column(3, Board()), "2")

    def test_choose_column_medium(self):
        self.ai_player.difficulty = "medium"
        self.ai_player.board.grid = [
            [None, None, None],
            [1, 1, None],
            [None, None, None],
        ]
        self.assertEqual(self.ai_player.choose_column(1, Board()), "2")

    def test_choose_column_hard(self):
        self.ai_player.difficulty = "hard"
        self.ai_player.board.grid = [
            [None, None, None],
            [1, 1, None],
            [None, None, None],
        ]
        opponent_board = Board()
        opponent_board.grid = [[None, None, None], [1, 1, None], [None, None, None]]
        self.assertEqual(self.ai_player.choose_column(1, opponent_board), "2")


class TestKnucklebone(unittest.TestCase):
    def setUp(self):
        self.game = Knucklebone()

    def test_get_current_player(self):
        self.game.players = [Player("blue", "Alice"), Player("red", "Bob")]
        self.assertEqual(self.game.get_current_player().name, "Alice")
        self.game.current_turn_index = 1
        self.assertEqual(self.game.get_current_player().name, "Bob")

    @patch("random.choice")
    def test_random_number(self, mock_choice):
        mock_choice.return_value = "4"
        self.assertEqual(self.game.random_number(), "4")

    def test_end_turn(self):
        self.game.current_turn_index = 0
        self.game.end_turn()
        self.assertEqual(self.game.current_turn_index, 1)
        self.game.end_turn()
        self.assertEqual(self.game.current_turn_index, 0)

    def test_is_game_over(self):
        self.game.players = [Player("blue", "Alice"), Player("red", "Bob")]
        self.assertFalse(self.game.is_game_over())
        self.game.players[0].board.grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.assertTrue(self.game.is_game_over())

    def test_clear_opponent_column(self):
        self.game.players = [Player("blue", "Alice"), Player("red", "Bob")]
        opponent = self.game.players[1 - self.game.current_turn_index]
        opponent.board.grid = [[1, 2, 3], [4, 4, 4], [7, 8, 9]]
        self.game.clear_opponent_column("2", "4")
        self.assertEqual(opponent.board.grid[1], [None, None, None])


if __name__ == "__main__":
    unittest.main()
