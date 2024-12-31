from tkinter import *
import pandas as pd
from pandas.core.internals.construction import dataclasses_to_dicts
import random

BACKGROUND_COLOR = "#B1DDC6"



# ---------------------------- DATA ------------------------------- #

data_dict = {}

try:
    data = pd.read_csv("data/french_words.csv")
    data_dict = data.to_dict(orient="records")
    print(data_dict)
except FileNotFoundError:
    print("ERROR - The file wasn't found.")
except pd.errors.EmptyDataError:
    print("ERROR - The CSV file is empty.")
except Exception as e:
    print(f"ERROR - : An error occurred: {e}")

current_word = {}



def next_card():
    global current_word, flip_timer
    window.after_cancel(flip_timer)
    current_word = random.choice(data_dict)
    canvas.itemconfig(card_image, image=card_front_img)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_word["French"], fill="black")
    window.after(3000, func=flip_card)





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









# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)


flip_timer = window.after(3000, func=flip_card)



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
known_button = Button(image=check_img, highlightthickness=0, command=next_card)
known_button.grid(row = 1, column = 1)




window.mainloop()

