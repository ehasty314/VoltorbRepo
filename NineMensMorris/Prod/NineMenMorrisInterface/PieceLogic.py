#todo add moveValidator,
import Record



class Locations:
    def __init__(self):
        # 24 positions initialized to 0 (empty)
        self.board = [0] * 24
        self.current_player = 1  # Start with player 1
        # Define valid positions on the board
        self.valid_positions = set(range(24))
        # Track total number of pieces for each player
        self.piece_count = {1: 9, 2: 9}
        # Track how many pieces have been placed on the board
        self.pieces_placed = {1: 0, 2: 0}
        #active turn count
        self.turn_count = 0
        #value for player phases: 1 is placing pieces, 2 is moving pieces, 3 is flying pieces
        self.player_phases = {1: 1, 2: 1}
        self.player_mills = {1: [], 2: []}
        self.can_remove = False
        self.log = Record()

        

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
            log.place_piece(self.current_player,position)
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
        log.movepiece(self.current_player,from_position,to_position)
        return True

    def switch_player(self):
        """
        Switch the current player.
        """
        self.current_player = 3 - self.current_player  # Switches between 1 and 2


    def update_mill(self):
   # upkeeps list of mills for each player. returns True If a new mill has formed since last update.
   # assumption this method is called after every click
        mills = [
                [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontal mills in the outer square
                [9, 10, 11], [12, 13, 14], [15, 16, 17],  # Horizontal mills in the middle square
                [18, 19, 20], [21, 22, 23],  # Horizontal mills in the inner square
                [0, 9, 21], [3, 10, 18], [6, 11, 15],  # Vertical mills in the left side
                [1, 4, 7], [16, 19, 22],  # Vertical mills in the middle
                [8, 12, 17], [5, 13, 20], [2, 14, 23]  # Vertical mills in the right side
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
        :param position: int, position on the board (0-23)
        :return: bool, True if the piece was removed successfully, False otherwise
        """
        opponent = 3 - self.current_player
        mill_remove = True
        if self.board[position] == opponent:
            if position in self.player_mills[opponent]:
                # if we try to remove a piece in an opponents mill, check to see if there are any pieces
                # that are not in the opponents mill.
                # if there is then do not allow removal. Otherwise allow
                for piece in self.board:
                    if piece == opponent:
                        for mill in self.player_mills[opponent]:
                            if piece not in mill:
                                mill_remove = False
                if mill_remove:
                    self.board[position] = 0
                    self.piece_count[3 - self.current_player] -= 1
                    self.pieces_placed[3 - self.current_player] -= 1
                    log.logRemove(self.current_player,position)
                    return True
                else:
                    print("Invalid removal. Try again.")
                    return False

            else:
                self.board[position] = 0
                self.piece_count[3 - self.current_player] -= 1
                self.pieces_placed[3-self.current_player] -= 1
                return True
        else:
            print("Invalid removal. Try again.")
            return False
    
    def move_piece(self, moveFrom, moveTo):
        # changed neighbors for our board, old neighbors below
        neighbors = {
        0: [1, 9],
        1: [0, 2, 4],
        2: [1, 14],
        3: [4, 10],
        4: [3, 1, 7, 5],
        5: [4, 13],
        6: [7, 11],
        7: [6, 4, 8],
        8: [7, 12],
        9: [0, 10, 21],
        10: [3, 9, 11, 18],
        11: [6, 10, 15],
        12: [8, 13, 17],
        13: [5, 12, 20, 14],
        14: [2, 13, 23],
        15: [11, 16],
        16: [15, 17, 19],
        17: [12, 16],
        18: [10, 19],
        19: [16, 18, 20, 22],
        20: [13, 19],
        21: [9, 22],
        22: [19, 21, 23],
        23: [14, 22]
        }
        if self.can_fly():
            return self.fly_piece(moveFrom,moveTo)
        else:
            if moveTo in neighbors.get(moveFrom, []) and self.board[moveTo] == 0 and self.current_player == self.board[moveFrom]:
                self.board[moveTo] = self.board[moveFrom]
                self.board[moveFrom] = 0
                log.movepiece(self.current_player,moveFrom,moveTo)
                return True
            else:
                print("Invalid Location.")
                return False

    def can_place_piece(self):
        if self.piece_count[self.current_player] > self.pieces_placed[self.current_player]:
            return True
        else:
            return False

    def can_fly(self):
        if self.piece_count[self.current_player] == 3:
            return True
        return False



    def is_game_over(self):
        """
        Check game state to see if game over has been accomplished
        """
        if self.piece_count.get(1) <= 2:
            log.writeFile()
            return True
        if self.piece_count.get(2) <= 2:
            log.writeFile()
            return True
        else:
            return False

    def increment_turn(self):
        self.turn_count += 1


        




