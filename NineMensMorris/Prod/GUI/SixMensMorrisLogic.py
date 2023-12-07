from Record import R


class SixMensMorrisLogic:
    def __init__(self):
        # 24 positions initialized to 0 (empty)
        self.board = [0] * 16
        self.current_player = 1  # Start with player 1
        # Define valid positions on the board
        self.valid_positions = set(range(16))
        # Track total number of pieces for each player
        self.piece_count = {1: 6, 2: 6}
        # Track how many pieces have been placed on the board
        self.pieces_placed = {1: 0, 2: 0}
        # active turn count
        self.turn_count = 0
        # value for player phases: 1 is placing pieces, 2 is moving pieces, 3 is flying pieces
        self.player_phases = {1: 1, 2: 1}
        self.player_mills = {1: [], 2: []}
        self.can_remove = False
        self.log = R()
        self.neighbors = {
            0: [1, 6],
            1: [0, 2, 4],
            2: [1, 9],
            3: [4, 7],
            4: [1, 3, 5],
            5: [4, 8],
            6: [0, 7, 13],
            7: [3, 10],
            8: [5, 9, 12],
            9: [2, 8, 15],
            10: [7, 11],
            11: [10, 12, 14],
            12: [8, 11],
            13: [6, 14],
            14: [11, 13, 15],
            15: [9, 14]
        }

    def place_piece(self, position):
        """
        Place a piece on the board.
        :param position: int, position on the board (0-23)
        :return: bool, True if the piece was placed successfully, False otherwise
        """

        if position in self.valid_positions and self.board[position] == 0:
            self.board[position] = self.current_player
            print(f"position: {position}, playerval: {self.board[position]}")
            self.pieces_placed[self.current_player] += 1
            self.log.logPlace(self.current_player, position)
            return True
        else:
            print("Invalid move. Try again.")
            return False


    def switch_player(self):
        """
        Switch the current player.
        """
        self.current_player = 3 - self.current_player  # Switches between 1 and 2

    def update_mill(self):
        # upkeeps list of mills for each player. returns True If a new mill has formed since last update.
        # assumption this method is called after every click
        mills = [
            [0, 1, 2], [0, 6, 13], [3, 4, 5], [10, 11, 12], [13, 14, 15], [2, 9, 15], [3, 7, 10], [5, 8, 12]
        ]
        new_mill = False
        for mill in mills:
            counts = 0
            for position in mill:
                # determine if a player has formed this mill
                if self.board[position] == 1:
                    counts += 1
                elif self.board[position] == 2:
                    counts -= 1
            if counts == 3 or counts == -3:
                # mill detected
                if counts >= 0:
                    if mill not in self.player_mills[1]:
                        self.player_mills[1].append(mill)
                        new_mill = True
                else:
                    if mill not in self.player_mills[2]:
                        self.player_mills[2].append(mill)
                        new_mill = True
            else:
                # no player has this mill currently. Update list of mills
                if mill in self.player_mills[1]:
                    self.player_mills[1].remove(mill)
                if mill in self.player_mills[2]:
                    self.player_mills[2].remove(mill)

        return new_mill

    def remove_opponent_piece(self, position):
        """
        Remove an opponent's piece from the board.
        param position int, position on the board (0-23)
        return bool, True if the piece was removed successfully, False otherwise
        """
        opponent = 3 - self.current_player
        if self.board[position] == opponent:
            # Check if the piece is part of a mill
            is_in_mill = any(position in mill for mill in self.player_mills[opponent])

            # Check if all opponent's pieces are in mills
            all_in_mills = all(any(pos in mill for mill in self.player_mills[opponent])
                               for pos, piece in enumerate(self.board) if piece == opponent)

            if is_in_mill and not all_in_mills:
                print("Cannot remove a piece from a mill unless all opponent's pieces are in mills.")
                return False
            else:
                # Remove the piece
                self.board[position] = 0
                self.piece_count[opponent] -= 1
                self.pieces_placed[opponent] -= 1
                self.log.logRemove(self.current_player, position)
                return True
        else:
            print("Invalid removal. Try again.")
            return False

    def move_piece(self, moveFrom, moveTo):
        # changed neighbors for our board, old neighbors below

        if moveTo in self.neighbors.get(moveFrom, []) and self.board[moveTo] == 0 and self.current_player == self.board[
            moveFrom]:
            self.board[moveTo] = self.board[moveFrom]
            self.board[moveFrom] = 0
            self.log.logMove(self.current_player, moveFrom, moveTo)
            return True
        else:
            print("Invalid Location.")
            return False

    def can_place_piece(self):
        if self.piece_count[self.current_player] > self.pieces_placed[self.current_player]:
            return True
        else:
            return False


    def is_game_over(self):
        """
        Check game state to see if game over has been accomplished
        """
        if self.piece_count.get(1) <= 2:
            self.log.writeFile()
            return True
        if self.piece_count.get(2) <= 2:
            self.log.writeFile()
            return True
        else:
            return False

    def increment_turn(self):
        self.turn_count += 1

    def is_valid_move_possible(self):
        # iterate through all board pieces
        for i in self.board:
            # if the current space belongs to the current player
            if i == self.current_player:
                # iterate through neighbors to find that spot
                for key, value in self.neighbors.items():
                    # check if the neighboring spots are occupied
                    for neighbor in value:
                        if self.board[neighbor] == 0 and not self.board[key]:
                            # The neighbor is not occupied, valid move is possible
                            return True
        # No valid moves found
        return False
