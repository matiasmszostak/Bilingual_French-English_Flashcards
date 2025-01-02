from tkinter import *
import pandas as pd
from pandas.core.internals.construction import dataclasses_to_dicts
import random

BACKGROUND_COLOR = "#B1DDC6"



# ---------------------------- DATA ------------------------------- #

words_to_learn = {}

try:
    data = pd.read_csv("data/words_to_learn.csv")
    print(words_to_learn)
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    words_to_learn = original_data.to_dict(orient="records")
except Exception as e:
    print(f"ERROR - : An error occurred: {e}")
else:
    words_to_learn = data.to_dict(orient="records")






current_word = {}



def next_card():
    global current_word, flip_timer
    if flip_timer is not None:
        window.after_cancel(flip_timer)
    if not words_to_learn:
        show_completion_message()
        return
    current_word = random.choice(words_to_learn)
    canvas.itemconfig(card_image, image=card_front_img)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_word["French"], fill="black")
    flip_timer = window.after(3000, func=flip_card)




def flip_card():

    current_title = canvas.itemcget(card_title, "text")

    if current_title == "French":
        canvas.itemconfig(card_image, image=card_back_img)
        canvas.itemconfig(card_title, text="English", fill="white")
        canvas.itemconfig(card_word, text=current_word["English"], fill="white")
    else:
        canvas.itemconfig(card_image, image=card_front_img)
        canvas.itemconfig(card_title, text="French", fill="black")
        canvas.itemconfig(card_word, text=current_word["French"], fill="black")




def is_known():
    try:
        words_to_learn.remove(current_word)
        df_words_to_learn = pd.DataFrame(words_to_learn)
        df_words_to_learn.to_csv("data/words_to_learn.csv", index=False)
    except Exception as e:
       print(f"ERROR - : An error occurred: {e}")
    if not words_to_learn:
        show_completion_message()
    else:
        next_card()

def show_completion_message():
    global flip_timer
    if flip_timer is not None:
        window.after_cancel(flip_timer)
    canvas.itemconfig(card_image, image=card_front_img)
    canvas.itemconfig(card_title, text="Congratulations!", fill="black")
    canvas.itemconfig(card_word, text="All words learned!", fill="black")



# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = None

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_image = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))

card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan = 2)

next_card()



# Buttons

cross_img = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_img, highlightthickness=0, command=next_card)
unknown_button.grid(row = 1, column = 0)

check_img = PhotoImage(file="images/right.png")
known_button = Button(image=check_img, highlightthickness=0, command=is_known)
known_button.grid(row = 1, column = 1)




window.mainloop()

