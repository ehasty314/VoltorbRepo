import unittest
from NineMensMorris.Prod.NineMenMorrisInterface.PieceLogic import Locations

class TestOccupiedLocations(unittest.TestCase):

    def setUp(self):
        self.game = Locations()

    def test_place_piece_valid(self):
        self.assertTrue(self.game.place_piece(0))
        self.assertEqual(self.game.board[0], 1)

    def test_place_piece_invalid(self):
        self.game.board[1] = 1
        self.assertFalse(self.game.place_piece(1))
        self.assertEqual(self.game.board[1], 1)

    def test_place_piece_on_same_space_opposing(self):
        self.game.place_piece(1)
        self.assertFalse(self.game.place_piece(1))

    def test_place_piece_on_same_space_current(self):
        self.game.place_piece(1)
        self.game.place_piece(2)
        self.assertFalse(self.game.place_piece(1))

    def test_place_piece_over_max(self):
        # could be dbc conflict
        for piece in range(9):
            self.game.place_piece(piece)
        self.assertFalse(self.game.place_piece(19))

    def can_place_piece_True(self):
        self.assertTrue(self.game.can_place_place_piece())

    def can_place_piece_FalseOutOfPieces(self):
        for piece in range(18):
            self.game.place_piece(piece)
        self.assertFalse(self.game.can_place_place_piece())

    def test_fly_piece_valid(self):
        self.game.board[0] = 1
        self.game.piece_count[1] = 3
        self.assertTrue(self.game.fly_piece(0, 1))
        self.assertEqual(self.game.board[0], 0)
        self.assertEqual(self.game.board[1], 1)

    def test_fly_piece_invalid(self):
        self.game.board[0] = 1
        self.game.piece_count[1] = 4
        self.assertFalse(self.game.fly_piece(0, 1))
        self.assertEqual(self.game.board[0], 1)
        self.assertEqual(self.game.board[1], 0)

    def test_switch_player(self):
        self.game.switch_player()
        self.assertEqual(self.game.current_player, 2)
        self.game.switch_player()
        self.assertEqual(self.game.current_player, 1)

    def test_is_mill_true(self):
        self.game.board[0] = 1
        self.game.board[1] = 1
        self.game.board[2] = 1
        self.assertTrue(self.game.is_mill())

    def test_mill_more_pieces(self):
        self.game.board[3] = 1
        self.game.board[9] = 2
        self.game.board[4] = 1
        self.game.board[19] = 1
        self.game.board[5] = 1
        self.assertTrue(self.game.is_mill())

    def test_is_mill_false(self):
        self.game.board[0] = 1
        self.game.board[1] = 2
        self.game.board[2] = 1
        self.assertFalse(self.game.is_mill())

    def test_remove_opponent_piece_valid(self):
        self.game.board[3] = 2
        self.game.current_player = 1
        self.assertTrue(self.game.remove_opponent_piece(3))
        self.assertEqual(self.game.board[3], 0)

    def test_remove_opponent_piece_invalid(self):
        self.game.board[3] = 1
        self.game.current_player = 1
        self.assertFalse(self.game.remove_opponent_piece(3))
        self.assertEqual(self.game.board[3], 1)

    def test_move_piece_valid(self):
        self.game.board[3] = 1
        self.game.current_player = 1
        self.assertTrue(self.game.move_piece(3,4))
        self.assertEqual(self.game.board[3],0)
        self.assertEqual(self.game.board[4],1)

    def test_move_piece_invalid(self):
        self.game.board[3] = 1
        self.game.current_player = 1
        self.assertTrue(self.game.move_piece(3,11))
        self.assertFalse(self.game.board[3],0)
        self.assertFalse(self.game.board[4],1)

if __name__ == '__main__':
    unittest.main()
