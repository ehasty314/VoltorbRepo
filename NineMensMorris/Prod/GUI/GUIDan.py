import tkinter as tk
import random
from tkinter import messagebox
from PieceLogic import Locations
from GUIReplay import Replay

class NineMansMorrisGUI(tk.Tk):
      def __init__(self):
        super().__init__()
        self.title('Nine Mans Morris')
        self.geometry('900x600')

        self.start_frame = StartFrame(self)
        #Testing
        self.start_frame.pack(expand=True)
        print("Start frame created and packed successfully")

class GameFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        # self.play_comp = play_comp

        self.game = Locations()
        self.buttons = {}
        self.button_pressed = False
        self.selected_piece = -1

    def switch_player_and_check_game_over(self):
        self.game.switch_player()
        self.game.turn_count += 1

        if not self.is_valid_move_possible() and self.game.turn_count > 2 and not self.game.can_fly():
            print('Game Over! Thanks for playing')
            self.destroy()
        elif self.game.is_game_over():
            print('Game Over! Thanks for playing')
            self.destroy()

    def play_vs_computer(self):
        self.playComp = True
        self.start_game()

    def play_vs_human(self):
        self.playComp = False
        self.start_game()

    def play_recording(self):
        self.playComp = False
        self.start_game()

    def start_game(self):
        # Remove the start screen and set up the game board
        self.start_frame.destroy()
        self.setup_board()

    def is_valid_move_possible(self):
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
        # iterate through all board pieces
        for i in self.game.board:
            # if the current space belongs to the current player
            if i == self.game.current_player:
                # iterate through neighbors to find that spot
                for key, value in neighbors.items():
                    # check if the neighboring spots are occupied
                    for neighbor in value:
                        if self.game.board[neighbor] == 0 and not self.game.board[key]:
                            # The neighbor is not occupied, valid move is possible
                            return True
        # No valid moves found
        return False

    def setup_board(self):
    # testing
      print("Setting up the board")
      valid_loc = [(0, 0), (0, 3), (0, 6), (1, 1), (1, 3), (1, 5), (2, 2), (2, 3), (2, 4),
                 (3, 0), (3, 1), (3, 2), (3, 4), (3, 5), (3, 6),
                 (4, 2), (4, 3), (4, 4), (5, 1), (5, 3), (5, 5), (6, 0), (6, 3), (6, 6)]

      for row in range(7):
        for col in range(7):
            if (row, col) in valid_loc:
                index = valid_loc.index((row, col))
                button = tk.Button(self, text=' ', width=10, height=3,
                                   command=lambda idx=index: self.handle_click(self.buttons[idx], idx))
                button.grid(row=row, column=col)
                self.buttons[index] = button
            else:
                tk.Label(self, text=' ', width=10, height=3).grid(row=row, column=col)
    #   self.bind_buttons()
    #
    # def bind_buttons(self):
    #   for index, button in self.buttons.items():
    #     button.config(command=lambda idx=index: self.handle_click(self.buttons[index],idx))

    def handle_click(self, button,index):
      print("handle_click called")
      
      if self.game.is_game_over():
        print('Game Over! Thanks for playing')
        self.master.destroy()
      elif self.game.can_remove:
        # always remove if possible
        print('remove opponent piece')
        self.handle_remove(button,index)
      else:
        if self.game.can_place_piece():
            # placing phase handling
            self.handle_place(button,index)
        else:
            # select a piece or move selected piece
            if self.selected_piece != -1:
                print('where do you want to move')
                self.handle_move(button,index)
            else:
                print('select a piece')
                self.handle_select(button,index)


    def handle_remove(self, button,index):
        print("handle_remove called")
        # GUI update and some logic, removing a piece is always end of turn
        if self.game.remove_opponent_piece(index):
            button.config(text=str(' '))
            print(f'player: {self.game.current_player} Pieces remaining: {self.game.piece_count[self.game.current_player] - self.game.pieces_placed[self.game.current_player]}')
            self.game.can_remove = False
            self.switch_player_and_check_game_over()
            # if self.playComp == True:
            #     self.computerMove()

    def handle_place(self, button, index):
        print("handle_place called")
        if self.game.place_piece(index):
            button.config(text=str(self.game.current_player))
            if self.game.update_mill():
                # update mills after every placement. If mill forms, the player can remove
                print('mill!')
                print(f'player {self.game.current_player} can remove an opponents piece')
                self.game.can_remove = True
            else:
                self.switch_player_and_check_game_over()
                # if self.playComp == True:
                #     self.computerMove()

    def handle_select(self,button, index):
        print("handle_select called")
        # select a piece to move if not already done
        if self.game.board[index] == self.game.current_player:
            self.selected_piece = index
            self.buttons[self.selected_piece].config(fg='red')
            print(f'current selected piece is index:{index} by player {self.game.current_player}')
        else:
            print('not your piece')

    def handle_move(self, button, newspace):
        print("handle_move called")
        if self.game.board[newspace] == self.game.current_player:
            # if the player selects another one of their own pieces, change selected piece
            self.buttons[self.selected_piece].config(fg='black')
            self.handle_select(button,newspace)
        else:
            if self.game.move_piece(self.selected_piece, newspace):
                # if a valid move occurs, then update the buttons, clear selected piece
                self.buttons[self.selected_piece].config(text=' ')
                self.buttons[newspace].config(text=str(self.game.current_player))
                self.buttons[self.selected_piece].config(fg='black')
                self.buttons[newspace].config(fg='black')
                print(f'Player: {self.game.current_player} moved from: {self.selected_piece} to: {newspace}')
                self.selected_piece = -1
                if self.game.update_mill():
                    # mill checking
                    print('mill!')
                    print(f'player {self.game.current_player} can remove an opponents piece')
                    self.game.can_remove = True
                else:
                    # if self.playComp == True:
                    #     self.computerMove()
                    self.switch_player_and_check_game_over()
                    
    def place_computer_piece(self):
        computer_pieces = [index for index, piece in enumerate(self.game.board) if piece == self.game.current_player]

        if computer_pieces:
            # Computer piece is already on the board, try to place a piece in a neighbor spot
            for piece_index in computer_pieces:
                neighbors = self.get_neighbors(piece_index)
                for neighbor in neighbors:
                    if self.game.board[neighbor] == 0:
                        # Place a piece in the empty neighbor spot
                        self.game.place_piece(neighbor)
                        return
        else:
            # Computer piece is not on the board, find an empty spot to place a piece
            empty_spots = [index for index, piece in enumerate(self.game.board) if piece == 0]
            if empty_spots:
                # Place a piece in a random empty spot
                random_spot = random.choice(empty_spots)
                self.game.place_piece(random_spot)

    def get_neighbors(self, index):
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
        return neighbors[index]
   
    def remove_random_player_piece(self):
        player_pieces = [index for index, piece in enumerate(self.game.board) if piece == self.game.current_player]
        if player_pieces:
            # Randomly select a player piece
            piece_to_remove = random.choice(player_pieces)
            self.game.remove_opponent_piece(piece_to_remove)            

    def move_computer_piece(self):
        computer_pieces = [index for index, piece in enumerate(self.game.board) if piece == self.game.current_player]
        
        if computer_pieces:
            # Randomly select a computer piece
            selected_piece = random.choice(computer_pieces)
            
            # Check neighbors for empty spaces and move if possible
            neighbors = self.get_neighbors(selected_piece)
            empty_neighbors = [neighbor for neighbor in neighbors if self.game.board[neighbor] == 0]
            
            if empty_neighbors:
                # Move the piece to a random empty neighbor
                new_position = random.choice(empty_neighbors)
                self.game.move_piece(selected_piece, new_position)


class StartFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        tk.Button(self, text="Play vs Computer", command=self.play_vs_computer).pack(pady=10)
        tk.Button(self, text="Play vs Human", command=self.play_vs_human).pack(pady=10)
        tk.Button(self, text="Play Recording", command=self.play_recording).pack(pady=10)

        self.game = None

    def play_vs_computer(self):
        self.master.withdraw()  # Hide the current frame
        self.game = GameFrame(self.master)
        self.game.pack()

    def play_vs_human(self):
        self.game = GameFrame(self.master)
        self.destroy()
        self.game.pack()

    def play_recording(self):
      self.master.withdraw()
      self.game = ReplayFrame(self.master)


class ReplayFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.replay = Replay()


if __name__ == '__main__':
    app = NineMansMorrisGUI()
    app.mainloop()