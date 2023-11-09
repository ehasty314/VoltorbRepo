import tkinter as tk
from tkinter import messagebox
from NineMensMorris.Prod.NineMenMorrisInterface.PieceLogic import Locations
class NineMansMorrisGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Nine Mans Morris')
        self.geometry('900x600')
        self.locations = Locations()  
        self.buttons = {}
        
        validLoc = [(0,0), (0,3), (0,6),
                    (1,1), (1,3), (1,5),
                    (2,2), (2,3), (2,4),
                    (3,0), (3,1), (3,2), (3,4), (3,5), (3,6),
                    (4,2), (4,3), (4,4),
                    (5,1), (5,3), (5,5),
                    (6,0), (6,3), (6,6)]



#while not first game and player wishes to continue
#increment game count++
#prompt player for pvp or p v comp
#if prompt for pvp(possibly its own class)
#   construct new board, 2 player objects
#   do phase 1, while no mills exist for either player and total placed pieces less than 18
#   Phase 1, player 1 places piece, validate location with piecelogic
#          player 2 places piece, validate location with piecelogic 
#          store recorded value to inmemory object(player|NotMoved|Move to position)
#          switch player
#   do phase 2 while player 1 has more than 3 pieces or player 2 has more than 3 pieces
#   Phase 2, next player after phase 1s turn
#         player moves along valid line to open location
#         piecelogic enforce only valid lines to valid spaces, else repeat move
#         if valid move store recorded value to inmemory object(player|Moved From|Move to position)
#         Piecelogic check that moved position creates new mill
#         if mill created then current player can select to remove other players piece
#             if valid piece to remove, remove piece with piece logic 
#             if valid other player piece removed, store recorded value to inmemory object(player|Moved From|Removed)
#         if player1 or player2 has less than 3 pieces, then break, else continue
#         switch player
#   Phase 3(possibly does not exist, but only exists as a flag in phase 2;  check canFly =1 in piecelogic, check in phase2 movements and allow fly logic)
#   Do phase 2, while player 1 or player 2 has more then 3 pieces
#         next player after phase 2s turn
#         player with canfly can use move any valid location from piece logic(possibly use place piece in piece logic?)
#         reiterate with phase 2 logic of mill check
#         
#   completion(move out of pvp to main while?)
#     add win count to winning player
#     write in memory record to csv
#     request if rewatch of game
#     if rewatch is true, list timestamps
#     request new game, if true reset, else break
#else if prompt for p v comp(possibly its own class)
#         



#else if prompt for p v comp(possibly its own class)
#construct new board, construct 1 player object, construct playercomp object

        for row in range(7):
            for col in range(7):
                if (row, col) in validLoc:
                    button = tk.Button(self, text='', width=10, height=3)
                    button.grid(row=row, column=col)
                    index = validLoc.index((row, col))
                    button.bind('<Button-1>', self.click(index))
                    self.buttons[index] = button

                    # self.buttons[index] = tk.Button(self, text=' ', width=10, height=3, command=lambda index=index: self.click(index))
                    # self.buttons[index].grid(row=row, column=col)
                else:
                    tk.Label(self, text=' ', width=10, height=3).grid(row=row, column=col)

    def click(self, position):
        def move(event):
            tempPlayer = self.locations.current_player
            if not self.locations.is_moving_phase:
                if self.locations.place_piece(position):
                    self.buttons[position].config(text=str(tempPlayer))
                    print(f"Piece placed by {self.locations.current_player} at position {position}")
                else:
                    print("Invalid move. Try again.")
                    messagebox.showinfo('Invalid', 'Invalid move. Try again.')
            else:
                if self.locations.selected_piece is None:
                    if self.locations.select_piece(position):
                        self.buttons[position]['relief'] = tk.SUNKEN
                else:
                    old_position = self.locations.selected_piece
                    if self.locations.move_piece(position):
                        self.buttons[old_position]['text'] = ''
                        self.buttons[old_position]['relief'] = tk.RAISED  # Reset the button relief
                        self.buttons[position]['text'] = '1' if self.locations.current_player == 1 else '2'
                    else:
                        print("Invalid move. Try again.")
                        messagebox.showinfo('Invalid', 'Invalid move. Try again.')

        return move

        # tempPlayer = self.locations.current_player
        # if self.locations.place_piece(position):
        #     self.buttons[position].config(text=str(tempPlayer))
        #     print(f"Piece placed by {self.locations.current_player} at position {position}")
        # else:
        #     print("Invalid move. Try again.")
        #     messagebox.showinfo('Invalid', 'Invalid move. Try again.')


if __name__ == '__main__':
    app = NineMansMorrisGUI()
    app.mainloop()

