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
        self.button_pressed = False
        
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
                    index = validLoc.index((row, col))
                    self.buttons[index] = tk.Button(self, text=' ', width=10, height=3, command=lambda index=index: self.check_player_turn(self.buttons[index], index, validLoc))
                    self.buttons[index].grid(row=row, column=col)
                else:
                    tk.Label(self, text=' ', width=10, height=3).grid(row=row, column=col)

    #need to add 3rd variable int for wait flags
    """def click(self, position, flag):
        tempPlayer = self.locations.current_player
         
        if flag == 0:
            if self.locations.place_piece(position):
                self.buttons[position].config(text=str(tempPlayer))
                print(f"Piece placed by {self.locations.current_player} at position {position}")
                self.Locations.increment_turn()
                print(self.locations.turn_count)
            else:
                print("Invalid move. Try again.")
                messagebox.showinfo('Invalid', 'Invalid move. Try again.')
            NineMansMorrisGUI.wait_window(NineMansMorrisGUI)
        #need to check at the end of every turn:
        #was piece placed mill
        if flag == 1:
            if self.locations.is_mill(position):
                #need to wait for new position selection
                NineMansMorrisGUI.wait_window()
                self.locations.remove_opponent_piece(position)
                    #need a function for removing a piece from opponent
            #check for player stage, place mode, move mode, fly mode
                #if in move or fly mode, wait for second click
                    #if moving, check that they have selected their own piece
                        #if yes, wait for second click
                            #make sure move from old position to new is valid
                    #if flying, check for own piece
                        #wait for second clicck
                            #if second position is valid, fly
                #else
                    #continue with piece placement
            #finalize pieces, then switch turn
        """
    def button_position(self, position):
        return position

    def check_player_turn(self, button, position, validLoc):
        
        #if the player still has pieces to place
        if self.locations.piece_count[self.locations.current_player] > self.locations.pieces_placed[self.locations.current_player]:
            #set phase to 1  (placing)
            self.locations.player_phases[self.locations.current_player] = 1
            print(self.locations.is_mill(position))
            #check to see if there is a mill before moving phase
            print(f"Position: {position}")
            if not self.locations.is_mill(position):
                if self.locations.place_piece(position):
                    print(f"Piece Placed by player {self.locations.current_player}")
                    
                    button.config(text=str(self.locations.current_player))
                    if self.button_pressed == False:
                        self.locations.pieces_placed[self.locations.current_player] += 1  
                    print(F"Player {self.locations.current_player} pieces placed: {self.locations.pieces_placed[self.locations.current_player]}")
                else:
                    self.locations.switch_player()
                
            #if there is a mill, proceed here.
            else:
                print("here1")
                for row in range(7):
                    for col in range(7):
                        if (row, col) in validLoc:
                            index = validLoc.index((row, col))
                            button.config(command=lambda index=index: self.second_click(index, validLoc))
                print("Mill!")
                print("select piece to remove")
                self.wait_for_second_button()
                print("here")
                self.locations.remove_opponent_piece(button)
                return
        #else, check if the player has placed all of their pieces
        elif self.locations.piece_count[self.locations.current_player] <= self.locations.pieces_placed[self.locations.current_player]:
            #is the player flying phase
            if self.locations.piece_count[self.locations.current_player] == 3:
                self.locations.player_phases[self.locations.current_player] = 3
                #call wait to get second position
                #secPosition = button.wait_variable(position)
                #self.fly_piece(button.index, secPosition.index)
                return
            else:
                self.locations.player_phases[self.locations.current_player] = 2
                #call wait to get second position
                tempButton = button

                self.wait_variable(button)
                if self.locations.move_piece(position, button):
                    button.config(text=str(self.locations.current_player))
                    tempButton.config(text=str(""))
        self.locations.switch_player()
        
    def second_click(self,index, validLoc):
        self.button_pressed = True
        self.reset_button_call()
        return index

    def reset_button_call(self, validLoc):
        for row in range(7):
            for col in range(7):
                if (row, col) in validLoc:
                    index = validLoc.index((row, col))
                    self.buttons[index].config(command=lambda index=index: self.check_player_turn(self.buttons[index], index))

    def wait_for_second_button(self):
        self.button_pressed = False
        app.wait_variable(self.button_pressed)

if __name__ == '__main__':
    app = NineMansMorrisGUI()
    app.mainloop()

