import tkinter as tk
from tkinter import messagebox
from NineMensMorris.Prod.NineMenMorrisInterface.PieceLogic import Locations

class NineMansMorrisGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Nine Mans Morris')
        self.geometry('900x600')
        self.game = Locations()
        self.buttons = {}
        self.button_pressed = False
        self.selected_piece = 0


        validLoc = [(0, 0), (0, 3), (0, 6),
                    (1, 1), (1, 3), (1, 5),
                    (2, 2), (2, 3), (2, 4),
                    (3, 0), (3, 1), (3, 2), (3, 4), (3, 5), (3, 6),
                    (4, 2), (4, 3), (4, 4),
                    (5, 1), (5, 3), (5, 5),
                    (6, 0), (6, 3), (6, 6)]

        for row in range(7):
            for col in range(7):
                if (row, col) in validLoc:
                    index = validLoc.index((row, col))
                    self.buttons[index] = tk.Button(self, text=' ', width=10, height=3, command=lambda index=index: self.handle_click(self.buttons[index], index))
                    self.buttons[index].grid(row=row, column=col)
                else:
                    tk.Label(self, text=' ', width=10, height=3).grid(row=row, column=col)

    def handle_click(self, button, index):
        if self.game.can_remove:
            print('remove opponent piece')
            self.handle_remove(button,index)
        else:
            if self.game.can_place_piece():
                self.handle_place(button,index)
            else:
                if self.selected_piece != 0:
                    print('where do you want to move')
                    self.handle_move(index)
                else:
                    print('select a piece')
                    self.handle_select(index)

    def handle_remove(self, button, index):
        if self.game.remove_opponent_piece(index):
            button.config(text=str(' '))
            print(f'player: {self.game.current_player} Pieces remaining: {self.game.piece_count[self.game.current_player] - self.game.pieces_placed[self.game.current_player]}')
            self.game.can_remove = False
            self.game.switch_player()

    def handle_place(self, button, index):
        if self.game.place_piece(index):
            button.config(text=str(self.game.current_player))
            if self.game.update_mill():
                print('mill!')
                print(f'player {self.game.current_player} can remove an opponents piece')
                self.game.can_remove = True
            else:
                self.game.switch_player()

    def handle_select(self,index):
        if self.game.board[index] == self.game.current_player:
            self.selected_piece = index
            self.buttons[self.selected_piece].config(fg='red')
            print(f'current selected piece is index:{index} by player {self.game.current_player}')
        else:
            print('not your piece')

    def handle_move(self,newspace):
        if self.game.board[newspace] == self.game.current_player:
            self.buttons[self.selected_piece].config(fg='black')
            self.handle_select(newspace)
        else:
            if self.game.move_piece(self.selected_piece, newspace):
                self.buttons[self.selected_piece].config(text=' ')
                self.buttons[newspace].config(text=str(self.game.current_player))
                self.buttons[self.selected_piece].config(fg='black')
                self.buttons[newspace].config(fg='black')
                self.selected_piece = 0
                if self.game.update_mill():
                    print('mill!')
                    print(f'player {self.game.current_player} can remove an opponents piece')
                    self.game.can_remove = True
                else:
                    self.game.switch_player()


if __name__ == '__main__':
    app = NineMansMorrisGUI()
    app.mainloop()