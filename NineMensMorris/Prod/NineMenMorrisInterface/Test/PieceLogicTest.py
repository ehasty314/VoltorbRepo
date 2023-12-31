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

    def test_can_place_piece_True(self):
        self.assertTrue(self.game.can_place_piece())

    def test_can_place_piece_FalseOutOfPieces(self):
        for piece in range(18):
            self.game.place_piece(piece)
            self.game.switch_player()
        self.assertFalse(self.game.can_place_piece())

    def test_can_place_piece_after_removal(self):
        self.game.place_piece(0)
        self.game.update_mill()
        self.game.switch_player()
        self.game.place_piece(15)
        self.game.update_mill()
        self.game.switch_player()
        self.game.place_piece(1)
        self.game.update_mill()
        self.game.switch_player()
        self.game.place_piece(8)
        self.game.update_mill()
        self.game.switch_player()
        self.game.place_piece(2)
        self.assertTrue(self.game.update_mill())
        self.assertTrue(self.game.remove_opponent_piece(8))
        self.game.switch_player()
        self.assertTrue(self.game.can_place_piece())


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

    def test_update_mill_true(self):
        self.game.board[0] = 1
        self.game.board[1] = 1
        self.game.board[2] = 1
        self.assertTrue(self.game.update_mill())

    def test_mill_more_pieces(self):
        self.game.board[3] = 1
        self.game.board[9] = 2
        self.game.board[4] = 1
        self.game.board[19] = 1
        self.game.board[5] = 1
        self.assertTrue(self.game.update_mill())

    def test_update_mill_false(self):
        self.game.board[0] = 1
        self.game.board[1] = 2
        self.game.board[2] = 1
        self.assertFalse(self.game.update_mill())

    def test_update_mill_create_then_remove_mill(self):
        self.game.board[0] = 1
        self.game.board[1] = 1
        self.game.board[2] = 1
        self.game.update_mill()
        self.game.board[2] = 0
        self.assertFalse(self.game.update_mill())

    def test_update_mill_no_new_mill(self):
        self.game.board[3] = 1
        self.game.update_mill()
        self.game.board[9] = 2
        self.game.update_mill()
        self.game.board[4] = 1
        self.game.update_mill()
        self.game.board[19] = 1
        self.game.update_mill()
        self.game.board[5] = 1
        self.game.update_mill()
        self.game.board[16] = 2
        self.assertFalse(self.game.update_mill())

    def test_update_mill_one_piece(self):
        self.game.board[3] = 1
        self.game.board[2] = 2
        self.assertFalse(self.game.update_mill())

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

    def test_remove_opponent_piece_invalid_in_opponents_mill(self):
        self.game.board[0] = 1
        self.game.board[1] = 1
        self.game.board[2] = 1
        self.game.board[9] = 1
        self.game.update_mill()
        self.assertFalse(self.game.remove_opponent_piece(1))

    def test_remove_opponent_piece_valid_opponent_all_mill(self):
        self.game.board[0] = 1
        self.game.board[1] = 1
        self.game.board[2] = 1
        self.game.update_mill()
        self.assertTrue(self.game.remove_opponent_piece(1))

    def test_move_piece_valid(self):
        self.game.board[3] = 1
        self.game.current_player = 1
        self.assertTrue(self.game.move_piece(3,4))
        self.assertEqual(self.game.board[3],0)
        self.assertEqual(self.game.board[4],1)

    def test_move_piece_valid_8_to_7(self):
        self.game.board[8] = 1
        self.assertTrue(self.game.move_piece(8,7))

    def test_move_piece_invalid_not_neighbor(self):
        self.game.board[18] = 1
        self.game.current_player = 1
        self.assertFalse(self.game.move_piece(18,20))
        self.assertEqual(self.game.board[18],1)
        self.assertEqual(self.game.board[20],0)

    def test_move_piece_invalid_moving_onto_opponent(self):
        self.game.board[18] = 1
        self.game.current_player = 1
        self.game.board[19] = 2
        self.assertFalse(self.game.move_piece(18,19))
        self.assertEqual(self.game.board[18],1)
        self.assertEqual(self.game.board[19],2)

    def test_move_piece_valid_fly(self):
        for i in range(18):
            self.game.place_piece(i)
            self.game.switch_player()
        for i in range(1,12,2):
            self.game.remove_opponent_piece(i)
            print(f'removed position: {i}')
        self.game.switch_player()
        print(f'player: {self.game.current_player}')
        self.assertTrue(self.game.can_fly())
        self.assertTrue(self.game.move_piece(13,1))
        self.assertEqual(self.game.board[13],0)
        self.assertEqual(self.game.board[1],2)

    def test_can_fly_valid(self):
        for i in range(18):
            self.game.place_piece(i)
            self.game.switch_player()
        for i in range(1,12,2):
            self.game.remove_opponent_piece(i)
        self.game.switch_player()
        self.assertTrue(self.game.can_fly())

    def test_can_fly_invalid_too_many(self):
        for i in range(18):
            self.game.place_piece(i)
            self.game.switch_player()
        for i in range(1,10,2):
            self.game.remove_opponent_piece(i)
        self.game.switch_player()
        self.assertFalse(self.game.can_fly())



if __name__ == '__main__':
    unittest.main()
