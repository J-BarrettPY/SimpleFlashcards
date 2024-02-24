from tkinter import *
import random
import csv
import os

class flashcard:
    def __init__(self, question, possible_answers, answer):
        self.question = question
        self.possible_answers = possible_answers
        self.answer = answer
        self.side_up = "Q"

def flip(flashcard_list, the_canvas, index_of_card):
    the_canvas.delete("all")
    current_on_screen = flashcard_list[index_of_card]
    the_canvas.create_rectangle(0, 0, 500, 500, fill="black", outline="")
    if current_on_screen.side_up == "Q":
        the_canvas.create_text(270, 170, width=530, font="Times 18 bold", text=current_on_screen.possible_answers, fill="lightgray")
        current_on_screen.side_up = "A"
    else:
        the_canvas.create_text(270, 170, width=530, font="Times 18 bold", text=current_on_screen.question, fill="lightgray")
        current_on_screen.side_up = "Q"
    global card_index
    card_index = index_of_card

def show_answer(flashcard_list, the_canvas, index_of_card):
    the_canvas.delete("all")
    current_on_screen = flashcard_list[index_of_card]
    the_canvas.create_rectangle(0, 0, 500, 500, fill="black", outline="")
    the_canvas.create_text(270, 170, width=530, font="Times 18 italic bold", text=current_on_screen.answer, fill="lightgreen")
    global card_index
    card_index = index_of_card

def next_card(flashcard_list, the_canvas, index_of_card):
    the_canvas.delete("all")
    the_canvas.create_rectangle(0, 0, 500, 500, fill="black", outline="")
    global card_index
    if index_of_card + 1 >= len(flashcard_list):
        card_index = 0
    else:
        card_index = index_of_card + 1
    next_card_on_screen = flashcard_list[card_index]
    the_canvas.create_text(270, 170, width=530, font="Times 18 bold", text=next_card_on_screen.question, fill="lightgray")
    next_card_on_screen.side_up = "Q"

def prev_card(flashcard_list, the_canvas, index_of_card):
    the_canvas.delete("all")
    the_canvas.create_rectangle(0, 0, 500, 500, fill="black", outline="")
    global card_index
    if index_of_card - 1 < 0:
        card_index = len(flashcard_list) - 1
    else:
        card_index = index_of_card - 1
    next_card_on_screen = flashcard_list[card_index]
    the_canvas.create_text(270, 170, width=530, font="Times 18 bold", text=next_card_on_screen.question, fill="lightgray")
    next_card_on_screen.side_up = "Q"

def change_button_color_on_hover(button, original_bg_color, hover_bg_color, original_fg_color, hover_fg_color):
    def on_enter(e):
        button['bg'] = hover_bg_color
        button['fg'] = hover_fg_color
    def on_leave(e):
        button['bg'] = original_bg_color
        button['fg'] = original_fg_color
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

def finalize(flashcard_list, select_label):
    random.shuffle(flashcard_list)
    select_label.destroy()
    the_canvas = Canvas(window, width=550, height=370, highlightthickness=0, bg="black")
    the_canvas.create_text(270, 170, width=530, font="Times 18 bold", text=flashcard_list[0].question, fill="lightgray")
    global card_index
    card_index = 0
    the_canvas.place(x=225, y=60)
    flip_button = Button(text="Flip Card", font=("fixedsys", 30), command=lambda: flip(flashcard_list, the_canvas, card_index), bg="#333333", fg="lightgray")
    flip_button.pack(side=BOTTOM, pady=40)
    change_button_color_on_hover(flip_button, "#333333", "#393939", "lightgray", "white")
    answer_button = Button(text="Answer", font=("fixedsys", 30), command=lambda: show_answer(flashcard_list, the_canvas, card_index), bg="#333333", fg="lightgray")
    answer_button.place(x=800, y=60)  # Adjusted placement here
    change_button_color_on_hover(answer_button, "#333333", "#393939", "lightgray", "white")
    next_button = Button(text="Next", font=("fixedsys", 30), command=lambda: next_card(flashcard_list, the_canvas, card_index), bg="#333333", fg="lightgray")
    next_button.place(x=640, y=491)
    change_button_color_on_hover(next_button, "#333333", "#393939", "lightgray", "white")
    prev_button = Button(text="Prev", font=("fixedsys", 30), command=lambda: prev_card(flashcard_list, the_canvas, card_index), bg="#333333", fg="lightgray")
    prev_button.place(x=250, y=491)
    change_button_color_on_hover(prev_button, "#333333", "#393939", "lightgray", "white")


def get_flashcards(filepath):
    try:
        the_file = open(filepath, "r")
        the_file.seek(0)
        the_reader = csv.reader(the_file)
        next(the_reader, None)
        flashcard_list = [flashcard(line[0], line[1], line[2]) for line in the_reader]
        the_file.close()
        finalize(flashcard_list, select_label)
    except Exception as e:
        print(f"Error: {e}")

def list_csv_files():
    global select_label
    select_label = Label(window, text="Select your flashcards", font=("fixedsys", 24), bg="#333333", fg="white")
    select_label.place(x=window.winfo_width() // 2 - select_label.winfo_reqwidth() // 2, y=20)
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]

    y_position = 80 + select_label.winfo_height()
    for file in csv_files:
        button = Button(window, text=file, font=("fixedsys", 15), command=lambda f=file: get_flashcards(f), bg="#444444", fg="white")
        button.place(x=window.winfo_width() // 2 - button.winfo_reqwidth() // 2, y=y_position)
        y_position += 40
        change_button_color_on_hover(button, "#444444", "#4e4e4e", "white", "white")

def start_game():
    start_button.destroy()
    start_label.destroy()
    list_csv_files()

window = Tk()
window.configure(bg="#333333")
window.resizable(False, False)
window.geometry("1001x601")
window.title("Simple Flashcards")
the_canvas = Canvas(window, width=1000, height=600, highlightthickness=0, bg="#333333")
the_canvas.place(x=0, y=0)
the_canvas.create_rectangle(0, 0, 1000, 600, fill="#222222", outline="")
start_label = Label(text="FLASHCARDS", font=("fixedsys", 155), bg="#333333", fg="white", pady=90)
start_label.place(x=245, y=100)
start_button = Button(text="START STUDYING", font=("fixedsys", 30), command=start_game, bg="#444444", fg="white", anchor=CENTER, padx=99)
start_button.place(x=246, y=450)
change_button_color_on_hover(start_button, "#444444", "#4e4e4e", "white", "white")
window.mainloop()
