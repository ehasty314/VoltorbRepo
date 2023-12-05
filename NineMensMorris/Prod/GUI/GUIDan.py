import tkinter as tk
from tkinter import messagebox
from PieceLogic import Locations

class NineMansMorrisGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Nine Mans Morris')
        self.geometry('900x600')

        # Start screen
        self.start_frame = tk.Frame(self)
        self.start_frame.pack(expand=True)

        # Buttons for selecting game mode
        tk.Button(self.start_frame, text="Play vs Computer", command=self.play_vs_computer).pack(pady=10)
        tk.Button(self.start_frame, text="Play vs Human", command=self.play_vs_human).pack(pady=10)
        tk.Button(self.start_frame, text="Play Recording", command=self.play_vs_human).pack(pady=10)

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
        x = 0
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
        validLoc = [(0, 0), (0, 3), (0, 6), (1, 1), (1, 3), (1, 5), (2, 2), (2, 3), (2, 4),
                    (3, 0), (3, 1), (3, 2), (3, 4), (3, 5), (3, 6),
                    (4, 2), (4, 3), (4, 4), (5, 1), (5, 3), (5, 5), (6, 0), (6, 3), (6, 6)]

        for row in range(7):
            for col in range(7):
                if (row, col) in validLoc:
                    index = validLoc.index((row, col))
                    self.buttons[index] = tk.Button(self, text=' ', width=10, height=3, command=lambda index=index: self.handle_click(self.buttons[index], index))
                    self.buttons[index].grid(row=row, column=col)
                else:
                    tk.Label(self, text=' ', width=10, height=3).grid(row=row, column=col)

    def handle_click(self, button, index):
        # logic flow for each click, helper functions to simplify
        if self.game.is_game_over():
            print('Game Over! Thanks for playing')
            self.destroy()
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
                    self.handle_move(index)
                else:
                    print('select a piece')
                    self.handle_select(index)

    def handle_remove(self, button, index):
        # GUI update and some logic, removing a piece is always end of turn
        if self.game.remove_opponent_piece(index):
            button.config(text=str(' '))
            print(f'player: {self.game.current_player} Pieces remaining: {self.game.piece_count[self.game.current_player] - self.game.pieces_placed[self.game.current_player]}')
            self.game.can_remove = False
            self.switch_player_and_check_game_over()
            # if self.playComp == True:
            #     self.computerMove()

    def handle_place(self, button, index):
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

    def handle_select(self,index):
        # select a piece to move if not already done
        if self.game.board[index] == self.game.current_player:
            self.selected_piece = index
            self.buttons[self.selected_piece].config(fg='red')
            print(f'current selected piece is index:{index} by player {self.game.current_player}')
        else:
            print('not your piece')

    def handle_move(self,newspace):
        if self.game.board[newspace] == self.game.current_player:
            # if the player selects another one of their own pieces, change selected piece
            self.buttons[self.selected_piece].config(fg='black')
            self.handle_select(newspace)
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
                    

   
                    

    
if __name__ == '__main__':
    app = NineMansMorrisGUI()
    app.mainloop()
