import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import json
import random
from PIL import Image, ImageTk

import player_class

CreatePlayerFrameBackgroundPath = 'images/back.jpg'
MainFrameBackgroundPath = 'images/back.jpg'
QuestionFrameBackgroundPath = 'images/back.jpg'
NoPhotoPath = 'images/no_photo.png'
NoImagePath = 'images/no_photo.png'
CorrectImagePath = 'images/correct.png'
IncorrectImagePath = 'images/incorrect.png'



class Window:
    def __init__(self, title='Main', width=600, height=600):
        self.width = width
        self.height = height
        self.size = f'{width}x{height}'
        self.display = tk.Tk()
        self.display.title(title)
        self.display.geometry(self.size)
        self.display.resizable(0, 0)

        self.question_frames = self.create_question_frames()
        self.frames = {'create_player': CreatePlayerFrame(self, 'Create new player', 'images/back.jpg')}

        self.frames.update(self.question_frames)
        self.active_frame('create_player')

    def start(self):
        self.display.mainloop()

    def create_main_frame(self, player):
        self.frames['main'] = MainFrame(self, "Main", player, self.question_frames.keys(), 'images/back.jpg')

    def active_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.activate()
        frame.change_title()

    def create_question_frames(self):
        question_frames = dict()

        file = open('questions.json', 'r', encoding='utf-8')
        questions = json.load(file)
        file.close()

        random.shuffle(questions)
        for question_id, question in enumerate(questions, 1):
            question_frames[question_id] = QuestionFrame(
                self, question_id, question['question'],
                question['answers'], question['img_path'], 'images/back.jpg'
            )
        return question_frames


class Frame:
    def __init__(self, window, title, background=None):
        self.window = window
        self.frame = ttk.Frame(window.display, width=window.width, height=window.height)
        self.title = title
        self.change_title()

        self.style = ttk.Style()
        self.style.configure('Tlabel', font=('Calibri', 14))
        self.set_background_image(background)
        self.frame.grid(row=0, column=0, sticky='nsew')

    def activate(self):
        self.frame.tkraise()

    def change_title(self):
        self.frame.master.title(self.title)

    def set_background_image(self, background):
        if background:
            image = ImageTk.PhotoImage(
                Image.open(background).resize((self.window.width, self.window.height), Image.ANTIALIAS))
            background_label = ttk.Label(self.frame, image=image)
            background_label.image = image
            background_label.place(x=0, y=0, relwidth=1, relheight=1)


class CreatePlayerFrame(Frame):
    def __init__(self, window, title, background=None):
        super().__init__(window, title, background)

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
        self.gender_filed = ttk.Combobox(self.frame, value=['Male', 'Female'])
        self.gender_filed.place(relx=0.01, rely=0.25, anchor=tk.NW)

        # Настройка поля для ввода фото
        photo_label = ttk.Label(self.frame, text='Player photo: ')
        photo_label.place(relx=0.4, rely=0.01, anchor=tk.NW)

        self.img_path = 'images/no_photo.png'
        photo = ImageTk.PhotoImage(Image.open(self.img_path).resize((350, 350), Image.ANTIALIAS))
        self.photo = ttk.Label(self.frame, image=photo)
        self.photo.image = photo
        self.photo.place(relx=0.4, rely=0.05, anchor=tk.NW)

        photo_button = ttk.Button(self.frame, text='Choose photo', command=self.choose_photo)
        photo_button.place(relx=0.4, rely=0.65, anchor=tk.NW)

        create_button = ttk.Button(self.frame, text='Create player', command=self.create_player)
        create_button.place(relx=0.8, rely=0.95, anchor=tk.NW)

    def choose_photo(self):
        self.img_path = filedialog.askopenfilename(
            master=self.frame, title='Select player photo', filetypes=(('Image files', '*.png *.jpg'),)
        )
        photo = ImageTk.PhotoImage(Image.open(self.img_path).resize((350, 350), Image.ANTIALIAS))
        self.photo.configure(image=photo)
        self.photo.image = photo

    def create_player(self):
        player = player_class.Player(
            self.name_filed.get(), int(self.age_filed.get()), self.gender_filed.get(), self.img_path
        )
        self.window.create_main_frame(player)
        self.window.active_frame('main')


class MainFrame(Frame):
    def __init__(self, window, title, player, question_ids, background_image=None):
        super().__init__(window, title, background_image)

        # question_ids = ['История', 'Математика', 'Герои']

        photo = ImageTk.PhotoImage(Image.open(player.img_path).resize((300, 300), Image.ANTIALIAS))
        player_photo = ttk.Label(self.frame, image=photo)
        player_photo.image = photo
        player_photo.place(relx=0.5, rely=0.35, anchor=tk.CENTER)

        player_name = ttk.Label(self.frame, text=f'Name: {player.name}', width=40)
        player_name.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

        player_age = ttk.Label(self.frame, text=f'Age: {player.age}', width=40)
        player_age.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        player_gender = ttk.Label(self.frame, text=f'Gender: {player.gender}', width=40)
        player_gender.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

        self.buttons = {}
        button_positions = [
            (0.2, 0.85), (0.5, 0.85), (0.8, 0.85),
            (0.2, 0.9), (0.5, 0.9), (0.8, 0.9),
            (0.2, 0.95), (0.5, 0.95), (0.8, 0.95),
        ]
        for i, question_id in enumerate(question_ids):
            position = button_positions[i]
            rel_x, rel_y = position
            button = ttk.Button(self.frame, text=f'Question №{i + 1}', width=15)
            button.id = question_id
            button.bind('<Button-1>', self.show_question)
            button.place(relx=rel_x, rely=rel_y, anchor=tk.CENTER)
            self.buttons[question_id] = button

    def show_question(self, event):
        button = event.widget
        question_id = button.id
        self.window.active_frame(question_id)


class QuestionFrame(Frame):
    def __init__(self, window, question_id, question, answers, img_path, background=None):
        title = f'Question №{question_id}'

        super().__init__(window, title, background)


        img_path = img_path if img_path else NoImagePath
        question_img = ImageTk.PhotoImage(Image.open(img_path).resize((300, 300), Image.ANTIALIAS))
        question_image = ttk.Label(self.frame, image=question_img)
        question_image.image = question_img
        question_image.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        self.id = question_id

        question_text = ttk.Label(
            self.frame, text=question, border=2, relief=tk.SUNKEN, justify=tk.CENTER, wraplength=550
        )
        question_text.place(relx=0.5, rely=0.65, anchor=tk.CENTER)


        back_button = ttk.Button(self.frame, text="Back", command=self.go_back)
        back_button.place(relx=0.5, rely=0.95, anchor=tk.CENTER)

        self.buttons = self.create_buttons(answers)
        self.correct_img = ImageTk.PhotoImage(Image.open(CorrectImagePath).resize((17,17), Image.ANTIALIAS))
        self.incorrect_img = ImageTk.PhotoImage(Image.open(IncorrectImagePath).resize((17, 17), Image.ANTIALIAS))

    def create_buttons(self, answers):
        answers_values = list(answers.items())
        random.shuffle(answers_values)
        places = [(0.2, 0.8), (0.8, 0.8), (0.2, 0.9), (0.8, 0.9)]
        buttons = list()
        for index, answers_values in enumerate(answers_values):
            answer, value = answers_values
            rel_x, rel_y = places[index]
            button = ttk.Button(self.frame, text=answer, width=20)
            button.id = value
            button.bind('<Button-1>', self.check)
            button.place(relx=rel_x, rely=rel_y, anchor=tk.CENTER)
            buttons.append(button)
        return buttons

    def check(self, event):
        button = event.widget
        if button.id:
            button.configure(image=self.correct_img, compound=tk.LEFT)
        else:
            button.configure(image=self.incorrect_img, compound=tk.LEFT)
        # self.go_back()
    def go_back(self):
        self.window.active_frame('main')


if __name__ == '__main__':
    game = Window()
    game.start()
