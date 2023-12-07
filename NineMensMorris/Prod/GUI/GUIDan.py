import tkinter as tk

from NineMensMorris.Prod.GUI.NineMensMorrisGUI import GameFrame
from GUIReplay import Replay
from SixMensMorrisGUI import SixMensMorris

class NineMansMorrisGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Nine Mans Morris')
        self.geometry('900x600')

        self.start_frame = StartFrame(self)
        #Testing
        self.start_frame.pack(expand=True)
        print("Start frame created and packed successfully")

class StartFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        tk.Button(self, text="Play vs Computer", command=self.play_vs_computer).pack(pady=10)
        tk.Button(self, text="Play vs Human", command=self.play_vs_human).pack(pady=10)
        tk.Button(self, text="Play Recording", command=self.play_recording).pack(pady=10)

        self.game = None

    def play_vs_computer(self):
        self.game = WhichMorris(self.master, play_comp=True)
        self.destroy()
        self.game.pack()

    def play_vs_human(self):
        self.game = WhichMorris(self.master, play_comp=False)
        self.destroy()
        self.game.pack()

    def play_recording(self):
        self.master.withdraw()
        self.game = ReplayFrame(self.master)


class WhichMorris(tk.Frame):
    def __init__(self, master, play_comp):
        super().__init__(master)
        self.master = master
        self.play_comp = play_comp

        tk.Button(self, text="Play Six Mens Morris", command=self.play_six).pack(pady=10)
        tk.Button(self, text="Play Nine Mens Morris", command=self.play_nine).pack(pady=10)

        self.game = None
        self.frame = None
        self.button = None

    def new_game_button(self):
        new_game_button = tk.Button(self.master, text='New Game', width=10, height=1, command=lambda: self.restart_game())
        new_game_button.pack(pady=10)
        self.button = new_game_button

    def restart_game(self):
        self.frame = StartFrame(self.master)
        self.frame.pack()
        self.game.destroy()
        self.destroy()
        self.button.destroy()

    def play_six(self):
        self.game = SixMensMorris(self.master, self.play_comp)
        self.new_game_button()
        self.destroy()
        self.game.pack()

    def play_nine(self):
        self.game = GameFrame(self.master, self.play_comp)
        self.new_game_button()
        self.destroy()
        self.game.pack()


class ReplayFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.replay = Replay()


if __name__ == '__main__':
    app = NineMansMorrisGUI()
    app.mainloop()