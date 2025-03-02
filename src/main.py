from questions import *

from tkinter import *
import random

BG_COLOR = "#222222"
OPTION_COLOR = "#2c2c2c"
HOVER_COLOR = "#535353"

root = Tk()
root.geometry("600x600")
root.config(bg=BG_COLOR)

problem_chosen = None

# app GUI
def app() -> None:
    global problem_set_label
    global problem_number_label
    
    problem_frame = Frame(root,
                          bg=BG_COLOR,)
    problem_frame.pack(pady=(150, 0))
    problem_set_label = Label(problem_frame,
                              bg=BG_COLOR,
                              fg="#dedac1",
                              font=("Arial", 25))
    problem_set_label.pack(side=TOP,
                           pady=(0, 15))
    problem_number_label = Label(problem_frame,
                                 bg=BG_COLOR,
                                 fg="#dedac1",
                                 font=("Arial", 50))
    problem_number_label.pack()
    
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
                         command=lambda: next_question("fail"),)
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
                         command=lambda: next_question(),)
    pass_button.bind("<Enter>", func=lambda e: on_button_hover(pass_button))
    pass_button.bind("<Leave>", func=lambda e: on_button_hover(pass_button))
    pass_button.pack()

    def on_button_hover(button) -> None:
        button.bind("<Enter>", func=lambda e: button.config(bg=HOVER_COLOR))
        button.bind("<Leave>", func=lambda e: button.config(bg=OPTION_COLOR))
  
def next_question(option: str=None) -> None:
    global problem_chosen
    
    # if there are any questions marked wrong
    if len(questions_mark_wrong) > 0:
        for question in questions_mark_wrong:
            question_data = questions_mark_wrong[question]
            # subtract the countdown
            question_data["count"] -= 1
            # if countdown is zero
            if question_data["count"] <= 0:
                # add the question back into rotation
                questions_in_rotation.append(question_data["problem"])
                del questions_mark_wrong[question]
                break
    
    # if you fail the question
    if option == "fail":
        # set the counter to 5
        questions_mark_wrong[str(problem_chosen)] = {
            "problem": problem_chosen,
            "count": 5
        }
        
        # TODO: find all the questions marked with the same sub-topic
        # and randomly add one to the questions in rotation
    
    # clears any potential topics to be chosen
    topics_to_be_chosen.clear()
    
    # list of the total number of questions
    all_question_count = [
        count for count in topic_count.values()
    ]
    for topic, count in topic_count.items():
        # if a specific topic is not appearing enough,
        # add it to the potential topics to be chosen
        if count <= min(all_question_count) + 1:
            topics_to_be_chosen.append(topic)
    
    # chooses a random topic
    topic_chosen = random.choice(topics_to_be_chosen)
    # increase the number of times the problem has been chosen
    # (higher number means less chance of being picked)
    topic_count[topic_chosen] += 1
    # chooses a random problem set from the topic chosen
    set_chosen = random.choice(question_bank[topic_chosen])
    
    for set, question in set_chosen.items():
        # chooses a random question from the problem set
        set_and_question = [set, random.choice(question)]
        questions_in_rotation.append(set_and_question)
    
    # chooses a random question from the list of
    # current questions in rotation
    problem_chosen = random.choice(questions_in_rotation)
    
    set_label = problem_chosen[0]
    problem_label = problem_chosen[1]
    
    questions_in_rotation.remove(problem_chosen)
    
    # updates the current question display
    problem_set_label.config(text=set_label)
    problem_number_label.config(text=list(problem_label))
    
    print("Questions marked wrong:", questions_mark_wrong)
    print("Questions in rotation:", questions_in_rotation)
    print("Amount of times topic has appeared:", topic_count)
    print("=====================================")

if __name__ == "__main__":
    app()
    next_question()
    root.mainloop()