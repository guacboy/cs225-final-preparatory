from questions import *

from tkinter import *
import random
import json

BG_COLOR = "#222222"
OPTION_COLOR = "#2c2c2c"
HOVER_COLOR = "#535353"

root = Tk()
root.geometry("600x600")
root.config(bg=BG_COLOR)

# app GUI
def app() -> None:
    global problem_set_label
    global problem_number_label
    global choice_frame
    
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
                      pady=(0, 40))
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
                     padx=(0, 40))
    skip_button = Button(choice_frame,
                         bg=OPTION_COLOR,
                         fg="#eef1fa",
                         activebackground=HOVER_COLOR,
                         activeforeground="#eef1fa",
                         font=("Arial", 25),
                         padx=30,
                         pady=10,
                         text="➤",
                         command=lambda: next_question("skip"),)
    skip_button.bind("<Enter>", func=lambda e: on_button_hover(skip_button))
    skip_button.bind("<Leave>", func=lambda e: on_button_hover(skip_button))
    skip_button.pack(side=LEFT,
                     padx=(0, 40))
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
    global question_count
    global current_question_chosen
    
    if question_count >= 10:
        # resets the question count
        question_count = 0
        
        # disables the choice buttons
        for choice in choice_frame.winfo_children():
            try:
                choice.config(state="disabled")
            except TclError:
                pass
        
        break_frame = Frame(root)
        break_frame.place(relx=0.22,
                          rely=0.20)
        take_break_label = Label(break_frame,
                                 text="BREAK TIME :)",
                                 font=("Arial", 25))
        take_break_label.pack(pady=(25,0))
        continue_button = Button(break_frame,
                                 text="CONTINUE",
                                 font=("Arial", 15),
                                 command=lambda: resume_study())
        continue_button.pack(side=BOTTOM,
                             pady=(0,15))
        break_BG = Label(break_frame,
                         width=50,
                         height=10)
        break_BG.pack()
        
        def resume_study() -> None:
            # enables the choice buttons
            for choice in choice_frame.winfo_children():
                try:
                    choice.config(state="active")
                except TclError:
                    pass
                
            break_frame.place_forget()
    
    if option != "skip":
        question_count += 1
    
    # opens the data file
    with open("data.json", "r") as file:
        data = json.load(file)
    
    # if there are any questions marked wrong
    if len(data["questions_mark_wrong"]) > 0:
        for question in data["questions_mark_wrong"]:
            print()
            # subtracts the countdown
            question["count"] -= 1
            # if countdown is zero
            if question["count"] <= 0:
                question_index = data["questions_mark_wrong"].index(question)
                # add the question back into rotation
                data["questions_in_rotation"].append(data["questions_mark_wrong"][question_index]["question"])
                data["questions_mark_wrong"].remove(question)
    
    # if you fail the question
    if option == "fail":
        # set the counter to 5
        # (when the counter is zero, the question will be back in rotation)
        data["questions_mark_wrong"].append({
            "question": current_question_chosen,
            "count": 5
        })
        
        topic = current_question_chosen[0]
        set = current_question_chosen[1]
        question = current_question_chosen[2]
        subtopic_marked_wrong = current_question_chosen[3]
        
        # chooses a random subtopic based on wrong question
        subtopics_to_be_chosen = [
            subtopic for subtopic in question_bank[topic][set]
            if subtopic[1] == subtopic_marked_wrong and subtopic[0] != question
        ]
        # if there are other questions similar
        if len(subtopics_to_be_chosen) > 0:
            subtopic_chosen = list(random.choice(subtopics_to_be_chosen))

            # adds the question into the rotation
            data["questions_in_rotation"].append([topic] + [set] + subtopic_chosen)
    
    # if there are less than three questions in rotation
    if len(data["questions_in_rotation"]) < 3:
        # list of amount of times a topic has appeared
        all_topic_count = [
            count for count in data["topic_count"].values()
        ]
        # if a specific topic is not appearing enough,
        # add it to the potential topics to be chosen
        topics_to_be_chosen = [
            topic for topic, count in data["topic_count"].items() if count <= min(all_topic_count) + 1
        ]
        # chooses a random topic
        topic_chosen = random.choice(topics_to_be_chosen)
        # increase the number of times the topic has been chosen
        # (higher number means less chance of being picked)
        if option != "skip":
            data["topic_count"][topic_chosen] += 1
            
        # chooses a random set from the topic chosen
        sets_to_be_chosen = [
            set for set in question_bank[topic_chosen].keys()
        ]
        set_chosen = random.choice(sets_to_be_chosen)
        
        # chooses a random question from the set and topic chosen
        questions_to_be_chosen = [
            question for question in question_bank[topic_chosen][set_chosen]
        ]
        question_chosen = list(random.choice(questions_to_be_chosen))
        # adds the question chosen to be in rotation
        data["questions_in_rotation"].append([topic_chosen] + [set_chosen] + question_chosen)
    
    # chooses a random question from the list of questions in rotation
    current_question_chosen = random.choice(data["questions_in_rotation"])
    
    set_label = current_question_chosen[1]
    number_label = current_question_chosen[2]
    
    # updates the current question display
    problem_set_label.config(text=set_label)
    problem_number_label.config(text=number_label)
    
    # removes the question from rotation
    data["questions_in_rotation"].remove(current_question_chosen)
    
    # updates the data file
    with open("data.json", "w") as file:
        file.write(json.dumps(data, indent=4))

if __name__ == "__main__":
    # resets the question count
    question_count = 10
    
    app()
    next_question()
    root.mainloop()
    
    # opens the data file
    with open("data.json", "r") as file:
        data = json.load(file)
    
    # resets topic count
    for topic in data["topic_count"]:
        data["topic_count"][topic] = 0
    
    # updates the data file
    with open("data.json", "w") as file:
        file.write(json.dumps(data, indent=4))