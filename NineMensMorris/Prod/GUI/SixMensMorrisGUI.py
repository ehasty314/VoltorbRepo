import tkinter as tk
import random
from SixMensMorrisLogic import SixMensMorrisLogic
from GUIReplay import Replay


class SixMensMorris(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        # self.play_comp = play_comp

        self.game = SixMensMorrisLogic()
        self.buttons = {}
        self.button_pressed = False
        self.selected_piece = -1
        self.setup_board()


    def setup_board(self):
        # testing
        valid_loc = [(0, 0), (0, 2), (0, 4), (1, 1), (1, 2), (1, 3), (2, 0), (2, 1), (2, 3), (2, 4),
                     (3, 1), (3, 2), (3, 3), (4, 0), (4, 2), (4, 4)]

        canvas = tk.Canvas(self, width=900, height=600, background='grey')

        canvas.create_rectangle(25, 25, 360, 260, disabledfill='grey', outline='black', width=5)
        # canvas.create_rectangle(110, 80, 450, 310, disabledfill='grey', outline='black', width=5)
        canvas.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        for row in range(5):
            for col in range(5):
                if (row, col) in valid_loc:
                    index = valid_loc.index((row, col))
                    button = tk.Button(canvas, text=' ', width=10, height=3,
                                       command=lambda idx=index: self.handle_click(self.buttons[idx], idx))
                    button.grid(row=row, column=col)
                    self.buttons[index] = button
                else:
                    tk.Label(self, text=' ', width=10, height=3).grid(row=row, column=col)

    def handle_click(self, button, index):
        print("handle_click called")

        if self.game.is_game_over():
            print('Game Over! Thanks for playing')
            self.master.destroy()
        elif self.game.can_remove:
            # always remove if possible
            print('remove opponent piece')
            self.handle_remove(button, index)
        else:
            if self.game.can_place_piece():
                # placing phase handling
                self.handle_place(button, index)
            else:
                # select a piece or move selected piece
                if self.selected_piece != -1:
                    print('where do you want to move')
                    self.handle_move(button, index)
                else:
                    print('select a piece')
                    self.handle_select(button, index)

    def handle_remove(self, button, index):
        print("handle_remove called")
        # GUI update and some logic, removing a piece is always end of turn
        if self.game.remove_opponent_piece(index):
            button.config(text=str(' '))
            print(
                f'player: {self.game.current_player} Pieces remaining: {self.game.piece_count[self.game.current_player] - self.game.pieces_placed[self.game.current_player]}')
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

    def handle_select(self, button, index):
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
            self.handle_select(button, newspace)
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

    def switch_player_and_check_game_over(self):
        self.game.switch_player()
        self.game.turn_count += 1

        if not self.game.is_valid_move_possible() and self.game.turn_count > 2:
            print('Game Over! Thanks for playing')
            self.destroy()
        elif self.game.is_game_over():
            print('Game Over! Thanks for playing')
            self.destroy()
    #
    # def place_computer_piece(self):
    #     computer_pieces = [index for index, piece in enumerate(self.game.board) if piece == self.game.current_player]
    #
    #     if computer_pieces:
    #         # Computer piece is already on the board, try to place a piece in a neighbor spot
    #         for piece_index in computer_pieces:
    #             neighbors = self.get_neighbors(piece_index)
    #             for neighbor in neighbors:
    #                 if self.game.board[neighbor] == 0:
    #                     # Place a piece in the empty neighbor spot
    #                     self.game.place_piece(neighbor)
    #                     return
    #     else:
    #         # Computer piece is not on the board, find an empty spot to place a piece
    #         empty_spots = [index for index, piece in enumerate(self.game.board) if piece == 0]
    #         if empty_spots:
    #             # Place a piece in a random empty spot
    #             random_spot = random.choice(empty_spots)
    #             self.game.place_piece(random_spot)
    #
    # def get_neighbors(self, index):
    #     neighbors = {
    #         0: [1, 9],
    #         1: [0, 2, 4],
    #         2: [1, 14],
    #         3: [4, 10],
    #         4: [3, 1, 7, 5],
    #         5: [4, 13],
    #         6: [7, 11],
    #         7: [6, 4, 8],
    #         8: [7, 12],
    #         9: [0, 10, 21],
    #         10: [3, 9, 11, 18],
    #         11: [6, 10, 15],
    #         12: [8, 13, 17],
    #         13: [5, 12, 20, 14],
    #         14: [2, 13, 23],
    #         15: [11, 16],
    #         16: [15, 17, 19],
    #         17: [12, 16],
    #         18: [10, 19],
    #         19: [16, 18, 20, 22],
    #         20: [13, 19],
    #         21: [9, 22],
    #         22: [19, 21, 23],
    #         23: [14, 22]
    #     }
    #     return neighbors[index]
    #
    # def remove_random_player_piece(self):
    #     player_pieces = [index for index, piece in enumerate(self.game.board) if piece == self.game.current_player]
    #     if player_pieces:
    #         # Randomly select a player piece
    #         piece_to_remove = random.choice(player_pieces)
    #         self.game.remove_opponent_piece(piece_to_remove)
    #
    # def move_computer_piece(self):
    #     computer_pieces = [index for index, piece in enumerate(self.game.board) if piece == self.game.current_player]
    #
    #     if computer_pieces:
    #         # Randomly select a computer piece
    #         selected_piece = random.choice(computer_pieces)
    #
    #         # Check neighbors for empty spaces and move if possible
    #         neighbors = self.get_neighbors(selected_piece)
    #         empty_neighbors = [neighbor for neighbor in neighbors if self.game.board[neighbor] == 0]
    #
    #         if empty_neighbors:
    #             # Move the piece to a random empty neighbor
    #             new_position = random.choice(empty_neighbors)
    #             self.game.move_piece(selected_piece, new_position)


if __name__ == '__main__':
    app = tk.Tk()
    game = SixMensMorris(app)
    game.pack()
    app.mainloop()