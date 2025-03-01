from tkinter import *
import random

BG_COLOR = "#222222"
OPTION_COLOR = "#2c2c2c"
HOVER_COLOR = "#535353"

root = Tk()
root.geometry("600x600")
root.config(bg=BG_COLOR)

def app() -> None:
    problem_frame = Frame(root,
                          bg=BG_COLOR,)
    problem_frame.pack(pady=(150, 0))
    problem_set_label = Label(problem_frame,
                              bg=BG_COLOR,
                              fg="#dedac1",
                              font=("Arial", 25))
    problem_set_label.pack(side=TOP,
                           pady=(0, 15))
    problem_set_label.config(text="Exercise Set #9.2")
    problem_number_label = Label(problem_frame,
                                 bg=BG_COLOR,
                                 fg="#dedac1",
                                 font=("Arial", 50))
    problem_number_label.pack()
    problem_number_label.config(text="#1")
    
    choice_frame = Frame(root,
                         bg=BG_COLOR,
                         cursor="")
    choice_frame.pack(side=BOTTOM,
                      pady=(0, 50))
    fail_button = Button(choice_frame,
                         bg=OPTION_COLOR,
                         fg="#d02121",
                         activebackground=HOVER_COLOR,
                         activeforeground="#d02121",
                         font=("Arial", 25),
                         padx=30,
                         pady=10,
                         text="✖",
                         command=lambda:print("fail"),)
    fail_button.bind("<Enter>", func=lambda e: on_button_hover(fail_button))
    fail_button.bind("<Leave>", func=lambda e: on_button_hover(fail_button))
    fail_button.pack(side=LEFT,
                     padx=(0, 50))
    pass_button = Button(choice_frame,
                         bg=OPTION_COLOR,
                         fg="#31f75b",
                         activebackground=HOVER_COLOR,
                         activeforeground="#31f75b",
                         font=("Arial", 25),
                         padx=30,
                         pady=10,
                         text="✔",
                         command=lambda:print("pass"),)
    pass_button.bind("<Enter>", func=lambda e: on_button_hover(pass_button))
    pass_button.bind("<Leave>", func=lambda e: on_button_hover(pass_button))
    pass_button.pack()

def on_button_hover(button) -> None:
    button.bind("<Enter>", func=lambda e: button.config(bg=HOVER_COLOR))
    button.bind("<Leave>", func=lambda e: button.config(bg=OPTION_COLOR))

if __name__ == "__main__":
    app()
    root.mainloop()