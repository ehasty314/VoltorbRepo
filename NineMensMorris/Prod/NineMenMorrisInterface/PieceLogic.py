class Locations:
    def __init__(self):
        # 24 positions initialized to 0 (empty)
        self.board = [0] * 24
        self.current_player = 1  # Start with player 1
        # Define valid positions on the board
        self.valid_positions = set(range(24))
        # Track the number of pieces for each player
        self.piece_count = {1: 0, 2: 0}
        self.maxPieces = 9

    def place_piece(self, position):
        """
        Place a piece on the board.
        :param position: int, position on the board (0-23)
        :return: bool, True if the piece was placed successfully, False otherwise
        """
        if position in self.valid_positions and self.board[position] == 0 and self.piece_count[self.current_player] < self.maxPieces:
            self.board[position] = self.current_player
            self.piece_count[self.current_player] += 1  # Update piece count
            self.switch_player()
            return True
        else:
            print("Invalid move. Try again.")
            return False

    def fly_piece(self, from_position, to_position):
        """
        Fly a piece from one position to another.
        :param from_position: int, starting position (0-23)
        :param to_position: int, ending position (0-23)
        :return: bool, True if the piece was flown successfully, False otherwise
        """
        # Check if the player is allowed to fly a piece
        if self.piece_count[self.current_player] > 3:
            print("Cannot fly pieces unless you have only 3 pieces left.")
            return False
        # Check if the starting position contains the player's piece
        if self.board[from_position] != self.current_player:
            print("Invalid starting position.")
            return False
        # Check if the ending position is valid and empty
        if to_position not in self.valid_positions or self.board[to_position] != 0:
            print("Invalid ending position.")
            return False
        # Move the piece
        self.board[from_position] = 0
        self.board[to_position] = self.current_player
        self.switch_player()
        return True

    def switch_player(self):
        """
        Switch the current player.
        """
        self.current_player = 3 - self.current_player  # Switches between 1 and 2


    def is_mill(self, position):
        """
        Check if placing a piece in the given position forms a mill.
        :param position: int, position on the board (0-23)
        :return: bool, True if a mill is formed, False otherwise
        """
        # Define all possible mills
        mills = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontal mills in the outer square
            [9, 10, 11], [12, 13, 14], [15, 16, 17],  # Horizontal mills in the middle square
            [18, 19, 20], [21, 22, 23],  # Horizontal mills in the inner square
            [0, 9, 21], [3, 10, 18], [6, 11, 15],  # Vertical mills in the left side
            [1, 4, 7], [16, 19, 22],  # Vertical mills in the middle
            [8, 12, 17], [5, 13, 20], [2, 14, 23]  # Vertical mills in the right side
        ]
        for mill in mills:
            if position in mill:
                if all(self.board[pos] == self.current_player for pos in mill):
                    return True
        return False

    def remove_opponent_piece(self, position):
        """
        Remove an opponent's piece from the board.
        :param position: int, position on the board (0-23)
        :return: bool, True if the piece was removed successfully, False otherwise
        """
        opponent = 3 - self.current_player
        if self.board[position] == opponent:
            self.board[position] = 0
            return True
        else:
            print("Invalid removal. Try again.")
            return False

# Example usage
game = Locations()

# Player 1 places a piece and forms a mill
game.place_piece(0)
game.place_piece(1)
game.place_piece(2)

# Check if a mill is formed
if game.is_mill(2):
    print("A mill is formed!")

# Player 2 places a piece
game.place_piece(3)

# Player 1 removes a piece of Player 2
game.remove_opponent_piece(3)


