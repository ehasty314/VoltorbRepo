#region TODO
#need to update filename to accept input hardcoded to user selection of files in log directory

#endregion

import tkinter as tk
from tkinter import messagebox
import csv
import os
import time

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
        self.current_play = 0
        self.setup_board()

    def setup_board(self):
        self.title('Nine Mans Morris')
        self.geometry('550x900')
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
        next_button.grid(row=8, column=0, columnspan=8, pady=10)

        prev_button = tk.Button(self, text="Previous", command=self.previous)
        prev_button.grid(row=7, column=0, columnspan=7, pady=10)

        log_dir = os.path.join(".", "Log")
        files = os.listdir(log_dir)
        self.list_button = tk.Listbox(self)
        self.list_button.grid(row=7, column=0, columnspan=3, pady=20)

        for name in files:
          self.list_button.insert('end', name)

        self.select_button = tk.Button(self, text="Select File", command=self.select_log)
        self.select_button.grid(row=8, column=0, columnspan=3, pady=10)
        
        self.delay_button = tk.Entry(self)
        self.delay_button.grid(row=12, column=0, columnspan=3, pady=10)

        self.auto_button = tk.Button(self, text="Automate Next", command=self.automate_next)
        self.auto_button.grid(row=11, column=0, columnspan=3, pady=10)

    def select_log(self):
        if self.list_button.curselection():
          self.data_list =self.writeLog(str(self.list_button.get(self.list_button.curselection())))
        self.row_count = len(self.data_list)
        self.select_button.config(state='disabled')
        self.list_button.config(state='disabled')

    def handle_click(self, index, value):
        self.buttons[index].config(text=value, state='disabled')

    def automate_next(self):
      delay = int(self.delay_button.get())

      if delay == 0:
        # Call next method continuously
        self.auto_button.config(state='disabled')
        self.continuous_automation()
      else:
        # Call next method with a delay
        self.auto_button.config(state='disabled')
        self.delayed_automation(delay)

    def continuous_automation(self):
      # Check if there are more moves
      if self.current_play < self.row_count:
        # Call next method and schedule the next call
        self.next()
        self.after(1000, self.continuous_automation)  # Adjust the delay as needed
      else:
        print("Game over")
        self.auto_button.config(state='normal')

    def delayed_automation(self, delay):
      # Check if there are more moves
      if self.current_play < self.row_count:
        # Call next method and schedule the next call with a delay
        self.next()
        self.after(delay * 1000, self.delayed_automation, delay)
      else:
        print("Game over")
        self.auto_button.config(state='normal')

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
