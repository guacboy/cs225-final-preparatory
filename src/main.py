from tkinter import *
import random

root = Tk()
root.geometry("600x600")
root.config(bg="#222222")

def app() -> None:
    problem_set_label = Label(root,
                              bg="#272822",
                              fg="#dedac1",)
    problem_set_label.pack()
    problem_set_label.config(text="test")
    
    fail_button = Button(root,
                         text="fail")
    fail_button.pack()
    
    pass_button = Button(root,
                         text="pass")
    pass_button.pack()

if __name__ == "__main__":
    app()
    root.mainloop()