from tkinter import *
import random
import pandas


BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/spanish_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


# ---------------------------- READ DATA ----------------------------#

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="Spanish", fill="black")
    canvas.itemconfig(card_word, text=current_card["Spanish"], fill="black")
    canvas.itemconfig(card_background, image=card_front)
    flip_timer = window.after(3000, func=flip_card)

# ---------------------------- SAVE PROGRESS ----------------------------#

def if_known():
    to_learn.remove(current_card)
    print(len(to_learn))
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()

# ---------------------------- FLIP CARD ----------------------------#

def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back)

# ---------------------------- GUI SETUP ----------------------------#


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_background = canvas.create_image(400, 263, image=card_front)
card_title = canvas.create_text(400, 150, text=f"", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text=f"", font=("Arial", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)


r_button = PhotoImage(file="images/right.png")
right_button = Button(image=r_button, highlightthickness=0, command=if_known)
right_button.grid(column=1, row=1)

w_button = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=w_button, highlightthickness=0, command=next_card)
wrong_button.grid(column=0, row=1)

next_card()

window.mainloop()
