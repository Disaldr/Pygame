import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk

import player_class


class Window:
    def __init__(self, title='Main', width = 600, height = 600):
        self.width = width
        self.height = height
        self.size = f'{width}x{height}'
        self.display = tk.Tk()
        self.display.title(title)
        self.display.geometry(self.size)
        self.display.resizable(0,0)

    def start(self):
        self.display.mainloop()


if __name__ == '__main__':
    game = Window()
    game.start()


class Frame:
    def __init__(self, window, title, background = None):
        self.window = window
        self.frame = ttk.Frame(window.display, width = window.width, height = window.height)
        self.title = title
        self.change_title()

        self.style = ttk.Style()
        self.style.configure('Tlabel', font=('Calibri', 14))
        self.set_background_image(background)
        self.frame.grid(row=0,cloumn=0, sticky='nsew')

    def activate(self):
        self.frame.tkraise()

    def change_title(self):
        self.frame.master.title(self.title)

    def set_background_image(self, background):
        if background:
            image = ImageTk.PhotoImage(Image.open(background).resize((self.window.width, self.window.height)), Image.ANTIALIAS)
            background_label = ttk.Label(self.frame, image=image)
            background_label.place(x=0,y=0)