from tkinter import *
from tkinter import messagebox 
from PIL import Image, ImageTk
import pandas
import random
import csv

BACKGROUND_COLOR = "#B1DDC6"
global french_word
french_word = None
english_word = None
words = None

try:
    data = pandas.read_csv("data/words_to_learn.csv")
    to_learn = data.to_dict(orient='records')
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")
    to_learn = data.to_dict(orient='records')

def return_french():
    global words, french_word, english_word
    words = random.choice(to_learn)
    french_word = words['French']
    english_word = words['English']
    canvas.itemconfig(background, image = front_card_background)
    canvas.itemconfig(language_text, text='French')
    canvas.itemconfig(word_text, text=french_word)
    right_button.config(state=DISABLED)
    wrong_button.config(state=DISABLED)
    return french_word

def return_english(word):
    global english_word
    canvas.itemconfig(background, image = back_card_background)
    canvas.itemconfig(language_text, text='English')
    canvas.itemconfig(word_text, text=english_word)
    right_button.config(state=NORMAL)
    wrong_button.config(state=NORMAL)

def count_down(number):
    if number > 0:
        canvas.itemconfig(count_down_number, text=f'{number}')
        window.after(1000, count_down, number-1)
    else:
        canvas.itemconfig(count_down_number, text='')
        return

def new_card():
    global french_word
    french_word = return_french()
    count_down(5)
    window.after(5000, return_english, french_word)

def check_answer(answer):
    if answer:
        global words
        delete_index = to_learn.index(words)
        del to_learn[delete_index]
        data = pandas.DataFrame(to_learn)
        data.to_csv("data\words_to_learn.csv", index=False)
    new_card()

# Window setup
window = Tk()
window.title("Password Manager")
window.config(padx=35, pady=35, bg=BACKGROUND_COLOR)
window.resizable(False, False)

# Card
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
back_card_background = PhotoImage(file='images/card_back.png')
front_card_background = PhotoImage(file='images/card_front.png')
background = canvas.create_image(400, 263, image = front_card_background)
language_text = canvas.create_text(400, 190, text="French", font=('arial', 40, 'bold'))
word_text = canvas.create_text(400, 250, text=return_french, font=('arial', 35, 'italic'))
count_down_number = canvas.create_text(400, 50, text='', font=('arial', 40, 'bold'))
canvas.grid(column=0, row=0, columnspan=2, rowspan=2)

# Buttons
correct_button_image = PhotoImage(file = "images/right.png")
right_button = Button(image=correct_button_image, highlightthickness=0, command=lambda:check_answer(True)) # Agregar a ambas para que manden como parametro si borrar on no la palabra 
right_button.grid(row=3, column=0)

wrong_button_image = PhotoImage(file = "images/wrong.png")
wrong_button = Button(image=wrong_button_image, highlightthickness=0, command=lambda:check_answer(False))
wrong_button.grid(row=3, column=1)

new_card()

window.mainloop()