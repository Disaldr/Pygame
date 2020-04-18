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
            image = ImageTk.PhotoImage(Image.open(background).resize((self.window.width, self.window.height), Image.ANTIALIAS))
            background_label = ttk.Label(self.frame, image=image)
            background_label.place(x=0,y=0 )

class CreatePlayerFrame(Frame):
    def __init__(self, window, title, background = None):
        super().__init__(window,title,background)

        # Настройка поля для ввода имени
        name_label = ttk.Label(self.frame, text='Player name: ')
        name_label.place(relx=0.01, rely=0.01, anchor=tk.NW)
        self.name_filed = ttk.Entry(self.frame)
        self.name_filed.place(relx=0.01, rely=0.05, anchor=tk.NW)

        # Настройка поля для ввода возраста
        age_label = ttk.Label(self.frame, text='Player age: ')
        age_label.place(relx=0.01, rely=0.1, anchor=tk.NW)
        self.age_filed = ttk.Entry(self.frame)
        self.age_filed.place(relx=0.01, rely=0.15, anchor=tk.NW)

        # Настройка поля для ввода пола
        gender_label = ttk.Label(self.frame, text='Player gender: ')
        gender_label.place(relx=0.01, rely=0.2, anchor=tk.NW)
        self.gender_filed = ttk.Combobox(self.frame, value=['Male','Female'])
        self.gender_filed.place(relx=0.01, rely=0.25, anchor=tk.NW)

        # Настройка поля для ввода фото
        photo_label = ttk.Label(self.frame, text='Player photo: ')
        photo_label.place(relx=0.4, rely=0.01, anchor=tk.NW)

        self.img_path = 'images/no_photo.png'
        photo = ImageTk.PhotoImage(Image.open(self.img_path).resize((350,350), Image.ANTIALIAS))
        self.photo = ttk.Label(self.frame, image = photo)
        self.photo.place(relx=0.4,rely=0.05, anchor=tk.NW)

    def choose_photo(self):
        self.img_path = filedialog.askopenfilename(
            master=self.frame, title = 'Select player photo', filetypes=(('Image files', '*.png *.jpg'),)
        )
        photo = ImageTk.PhotoImage(Image.open(self.img_path).resize((350,350), Image.ANTIALIAS))
        self.photo.configure(image=photo)
        self.photo.image = photo

    def create_player(self):
        player = player_class.Player(
            self.name_filed.get(), int(self.age_filed.get()), self.gender_filed.get(), self.img_path
        )