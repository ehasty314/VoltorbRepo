#region TODO
#need to update filename to accept input hardcoded to user selection of files in log directory
#update game over condition to work with ongoing main player selection screen in GUIdan
#Remove main from GUIRepaly and integrate this somehow into the GUIDan main loop
#Update GUIDan button play replay to actually be funcational rather than place holder
#endregion

import tkinter as tk
from tkinter import messagebox
import csv
import os

class Replay(tk.Tk):
    #region properties
    #columns
    action = 0
    player = 1
    startLocation = 2
    endingLocation = 3 

    row_count = 0
    #endregion

    def __init__(self, master=None):  
        super().__init__(master)
        self.master = master
        #need to update this from hardcoded to user selection of files in log
        file_name = '2023-12-01_17-45-32.txt'
        self.data_list = self.writeLog(file_name)
        self.row_count = len(self.data_list)
        self.current_play = 0
        self.setup_board()

    def setup_board(self):
        self.title('Nine Mans Morris')
        self.geometry('900x600')
        validLoc = [(0, 0), (0, 3), (0, 6), (1, 1), (1, 3), (1, 5), (2, 2), (2, 3), (2, 4),
                    (3, 0), (3, 1), (3, 2), (3, 4), (3, 5), (3, 6),
                    (4, 2), (4, 3), (4, 4), (5, 1), (5, 3), (5, 5), (6, 0), (6, 3), (6, 6)]

        self.buttons = []  

        for row in range(7):
            for col in range(7):
                if (row, col) in validLoc:
                    index = validLoc.index((row, col))
                    button = tk.Button(self, text=' ', width=10, height=3,
                                       command=lambda index=index: self.handle_click(index),
                                       state='disabled')
                    button.grid(row=row, column=col)
                    self.buttons.append(button)
                else:
                    tk.Label(self, text=' ', width=10, height=3).grid(row=row, column=col)

        next_button = tk.Button(self, text="Next", command=self.next)
        next_button.grid(row=7, column=0, columnspan=7, pady=10)

        prev_button = tk.Button(self, text="Previous", command=self.previous)
        prev_button.grid(row=8, column=0, columnspan=7, pady=10)

    def handle_click(self, index, value):
        self.buttons[index].config(text=value, state='disabled')

    def next(self):
        if self.current_play < self.row_count:
            row = self.data_list[self.current_play]

            if row[self.action] == "place":
                self.handle_click(int(row[self.endingLocation]), row[self.player])
            elif row[self.action] == "move":
                self.handle_click(int(row[self.startLocation]), ' ')
                self.handle_click(int(row[self.endingLocation]), row[self.player])
            elif row[self.action] == "remove":
                self.handle_click(int(row[self.endingLocation]), ' ')

            self.current_play += 1

        #need to change this to work with ongoing main player selection screen
        if self.current_play == self.row_count:
            print("Game over")

    def previous(self):
        if self.current_play > 0:
            self.current_play -= 1
            row = self.data_list[self.current_play]

            if row[self.action] == "place":
                self.handle_click(int(row[self.endingLocation]), ' ')
            elif row[self.action] == "move":
                self.handle_click(int(row[self.startLocation]), row[self.player])
                self.handle_click(int(row[self.endingLocation]), ' ')
            elif row[self.action] == "remove":
                self.handle_click(int(row[self.endingLocation]), row[self.player])

    def writeLog(self, file_name):
        data_list = []
        log_dir = os.path.join(".", "Log")
        # Check and create the directory if it doesn't exist
        if not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir)
                print(f"Directory created: {log_dir}")
            except Exception as e:
                print(f"Error creating directory: {e}")
                return

        file_path = os.path.join(log_dir, file_name)
        with open(file_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter='|')
            for row in reader:
                data_list.append(row)

        return data_list
