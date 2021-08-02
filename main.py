from tkinter import *
import pandas as pd
from random import choice

BACKGROUND_COLOR = "#B1DDC6"

# -------------------------CREATE NEW FLASHCARDS ----------------------- #
current_card = {}
list_of_dict = {}

try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    list_of_dict = original_data.to_dict(orient="records")
else:
    list_of_dict = data.to_dict(orient="records")


def pick_word():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = choice(list_of_dict)
    canvas.itemconfig(language_label, text='French', fill="black")
    canvas.itemconfig(word_label, text=current_card['French'], fill="black")
    canvas.itemconfig(canvas_image, image=front_img)
    flip_timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(canvas_image, image=back_img)
    canvas.itemconfig(language_label, text='English', fill="white")
    canvas.itemconfig(word_label, text=current_card['English'], fill="white")


# ---------------------------- SAVE PROGRESS --------------------------- #
def delete_word():
    list_of_dict.remove(current_card)
    to_learn = pd.DataFrame(list_of_dict)
    to_learn.to_csv("data/words_to_learn.csv", index=False)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front_img = PhotoImage(file="images/card_front.png")
back_img = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=front_img)
language_label = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
word_label = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# self.testButton = Button(self, text=" test", command=lambda:[funct1(),funct2()])

cross_img = PhotoImage(file="images/wrong.png")
cross_button = Button(image=cross_img, highlightthickness=0, command=pick_word)
cross_button.grid(row=1, column=0)

check_img = PhotoImage(file="./images/right.png")
check_button = Button(image=check_img, highlightthickness=0, command=lambda: [delete_word(), pick_word()])
check_button.grid(row=1, column=1)

pick_word()

window.mainloop()
