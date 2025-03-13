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

def app() -> None:
    """
    Main GUI
    """
    
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

def prepare_json() -> None:
    """
    Populates the data.json file
    """
    
    # opens the data file
    with open("data.json", "r") as file:
        data = json.load(file)
    
    for topic in question_bank:
        # if topic has not been added
        if topic not in data["topic_count"]:
            # adds topics from question bank
            data["topic_count"][topic] = {}
        for set in question_bank[topic].keys():
            # if set has not been added
            if set not in data["topic_count"][topic]:
                # adds sets from question bank
                data["topic_count"][topic].update({
                    set: {}
                })
            for question in question_bank[topic][set]:
                # if set has not been added
                if question[0] not in data["topic_count"][topic][set]:
                    # adds questions from question bank
                    data["topic_count"][topic][set].update({
                        question[0]: 0
                    })
    
    # updates the data file
    with open("data.json", "w") as file:
        file.write(json.dumps(data, indent=4))

def add_questions_to_rotation() -> None:
    """
    Adds question to rotation in a sorted order
    for each subtopic and based on the amount
    of times the question has been selected
    """
    
    # opens the data file
    with open("data.json", "r") as file:
        data = json.load(file)
    
    sorted_questions = []
    for topic in question_bank:
        for set in question_bank[topic]:
            for question in question_bank[topic][set]:
                question_count = data["topic_count"][topic][set][question[0]]
                # [set, question, subtopic, question count]
                sorted_questions.append([topic] + [set] + list(question) + [question_count])
    # sorts list by subtopic (in alphabetical order)
    sorted_questions.sort(key=lambda x: x[3])

    questions_with_same_subtopic = []
    for question in sorted_questions:
        # if the list is not empty
        if len(questions_with_same_subtopic) > 0:
            # if the current question's subtopic does not
            # match the targeted subtopic
            if question[3] != subtopic:
                # collects all the question counts
                all_question_count = [
                    count[4] for count in questions_with_same_subtopic
                ]
                # sorts the list to questions that have
                # not been selected recently
                question_to_be_chosen = [
                    q for q in questions_with_same_subtopic
                    if q[4] <= min(all_question_count)
                ]
                
                # chooses a random question
                question_chosen = random.choice(question_to_be_chosen)
                # and adds it to the rotation
                data["questions_in_rotation"].append(question_chosen)
                
                # increase the number of times
                # the topic, set, and question have been chosen
                # (higher number means less chance of being picked)
                topic_idx = question_chosen[0]
                set_idx = question_chosen[1]
                question_idx = question_chosen[2]
                data["topic_count"][topic_idx][set_idx][question_idx] += 1
                
                # clears for next subtopic list
                questions_with_same_subtopic.clear()
        
        # if the list is empty
        # (or it's the first question to be added)
        if len(questions_with_same_subtopic) <= 0:
            # assign the targeted subtopic
            subtopic = question[3]
        
        # if question's subtopic matches with targeted subtopic
        # and it's not in the list yet
        if (question[3] == subtopic
            and question not in questions_with_same_subtopic):
            # add the question to the list
            questions_with_same_subtopic.append(question)
    
    # updates the data file
    with open("data.json", "w") as file:
        file.write(json.dumps(data, indent=4))

def next_question(option: str=None) -> None:
    """
    Iterates to the next question in rotation
    """
    
    # opens the data file
    with open("data.json", "r") as file:
        data = json.load(file)
    
    if option != "skip":
        data["amount_of_questions_done_count"] += 1
    
    if data["amount_of_questions_done_count"] > 5:
        # resets the amount of questions done
        data["amount_of_questions_done_count"] = 0
        
        break_time()
    
    # if there are any questions marked wrong
    if len(data["questions_mark_wrong"]) > 0:
        for question in data["questions_mark_wrong"]:
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
        # set the counter
        # (when the counter is zero, the question will be back in rotation)
        data["questions_mark_wrong"].append({
            "question": data["current_question"],
            "count": 3
        })
        
        # adds a question (that is not the same as the current question)
        # of the same subtopic into rotation
        topic_chosen = data["current_question"][0]
        subtopic_marked_wrong = data["current_question"][3]
        
        # populates list of questions with the same subtopic marked wrong
        questions_with_same_subtopic = []
        for set in question_bank[topic_chosen]:
            for question in question_bank[topic_chosen][set]:
                subtopic = question[1]
                if subtopic_marked_wrong == subtopic:
                    question_count = data["topic_count"][topic_chosen][set][question[0]]
                    # [set, question, subtopic, question count]
                    questions_with_same_subtopic.append([topic_chosen] + [set] + list(question) + [question_count])

        # collects all the question counts
        all_subtopics_count = [
            count[4] for count in questions_with_same_subtopic
        ]
        # sorts the list to questions that have
        # not been selected recently
        # and are not the same as the question marked wrong
        subtopics_to_be_chosen = [
            q for q in questions_with_same_subtopic
            if q[4] <= min(all_subtopics_count) and q != data["current_question"]
        ]
        
        # if there are other questions available
        if len(subtopics_to_be_chosen) > 0:
            # chooses a random question of the related subtopic
            question_chosen = random.choice(subtopics_to_be_chosen)
            # and adds it to the rotation
            data["questions_in_rotation"].append(question_chosen)
    
    # adds new questions to rotation
    if len(data["questions_in_rotation"]) <= 0:
        add_questions_to_rotation()
    
    try:
        # chooses a random question from the list of questions in rotation
        data["current_question"] = random.choice(data["questions_in_rotation"])
        
        update_question_labels(data["current_question"])
        
        # removes the question from rotation
        data["questions_in_rotation"].remove(data["current_question"])
    except IndexError:
        break_time(True)
        return
        
    # updates the data file
    with open("data.json", "w") as file:
        file.write(json.dumps(data, indent=4))

def update_question_labels(current_question: list) -> None:
    """
    Updates the question labels
    to the current question
    """
    
    set_label = current_question[1]
    number_label = current_question[2]
    
    # updates the current question display
    problem_set_label.config(text=set_label)
    problem_number_label.config(text=number_label)

def break_time(is_rotation_done: bool=False) -> None:
    """
    Displays the break screen
    """
    
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
    
    # if all questions in rotation have been completed
    if is_rotation_done:
        take_break_label.config(text="ROTATION DONE\nGOOD JOB :)")
        continue_button.config(text="NEXT ROTATION",
                               command=lambda: [resume_study(), next_question()])
        
        # opens the data file
        with open("data.json", "r") as file:
            data = json.load(file)
        
        # resets the amount of questions done
        data["amount_of_questions_done_count"] = 0
        
        # updates the data file
        with open("data.json", "w") as file:
            file.write(json.dumps(data, indent=4))
    
    def resume_study() -> None:
        # enables the choice buttons
        for choice in choice_frame.winfo_children():
            try:
                choice.config(state="active")
            except TclError:
                pass

        break_frame.destroy()

if __name__ == "__main__":
    # opens the data file
    with open("data.json", "r") as file:
        data = json.load(file)
    
    app()
    prepare_json()
    
    # if this is the first time running
    if len(data["questions_in_rotation"]) <= 0:
        add_questions_to_rotation()
        next_question()
    # if this is NOT the first time running
    else:
        update_question_labels(data["current_question"])
        
    root.mainloop()
    
    # resets the amount of questions done
    data["amount_of_questions_done_count"] = 0
    
    # updates the data file
    with open("data.json", "w") as file:
        file.write(json.dumps(data, indent=4))
    
    # # resets the file
    # data["current_question"].clear()
    # data["amount_of_questions_done_count"] = 0
    # data["questions_in_rotation"].clear()
    # data["questions_mark_wrong"].clear()
    # data["topic_count"].clear()
    
    # # updates the data file
    # with open("data.json", "w") as file:
    #     file.write(json.dumps(data, indent=4))