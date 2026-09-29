from pathlib import Path
from tkinter import *
from pandas import DataFrame, read_csv
import random

# Constants
BACKGROUND_COLOR = "#B1DDC6"

# ---------------------------- CHANGE CARD FRONT ------------------------------- #
# Read the data from the CSV file
df = read_csv("Day 31/data/french_words.csv")
data_dict = df.to_dict(orient="records")

def take_new_card():
    if len(data_dict) == 0:
        return {
            'French': 'Done with all cards!',
            'English': 'Done with all cards!'
        }

    return random.choice(data_dict)

def change_card_front(correct):
    global current_card, flip_timer

    if correct:
        data_dict.remove(current_card)  # Remove the current card from the list if answered correctly

    current_card = take_new_card()

    window.after_cancel(flip_timer)  # Cancel the previous flip timer if it exists

    canvas.itemconfig(canvas_create_text, text="French", fill="black")
    canvas.itemconfig(canvas_create_text2, text=current_card["French"], fill="black")
    canvas.itemconfig(canvas_create_image, image=cfront)
    flip_timer = window.after(3000, show_card_back)  # Change card back after 3 seconds

# ---------------------------- SHOW CARD BACK ------------------------------- #
def show_card_back():
    canvas.itemconfig(canvas_create_text, text="English", fill="white")
    canvas.itemconfig(canvas_create_text2, text=current_card["English"], fill="white")
    canvas.itemconfig(canvas_create_image, image=cback)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)

cfront = PhotoImage(file="Day 31/images/card_front.png")
cback = PhotoImage(file="Day 31/images/card_back.png")
cright = PhotoImage(file="Day 31/images/right.png")
cwrong = PhotoImage(file="Day 31/images/wrong.png")

# Labels
canvas_create_image = canvas.create_image(400, 263, image=cfront)
canvas.grid(row=0, column=0, columnspan=2)

canvas_create_text = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
canvas_create_text2 = canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"))

# Buttons
right_button = Button(image=cright, highlightthickness=0, command=lambda: change_card_front(True))
right_button.grid(row=1, column=0)

flip_timer = window.after(3000, show_card_back)  # Change card back after 3 seconds

wrong_button = Button(image=cwrong, highlightthickness=0, command=lambda: change_card_front(False))
wrong_button.grid(row=1, column=1)

change_card_front(correct=False)  # Show the first card
window.mainloop()