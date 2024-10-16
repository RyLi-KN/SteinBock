import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time
import os

# Questions
questions = [
    "Kommst du unter der Woche morgens bouldern?",
    "Wenn wir in der Zukunft unter der Woche um 9 Uhr aufmachen, würdest du kommen?"
]

# Number of questions
num_questions = len(questions)

# Initialize the lists to store counts
yes_counts = [0]*num_questions
no_counts = [0]*num_questions


# File to store counts
file_path = "counts.txt"

# Load counts from the file if it exists
if os.path.exists(file_path):
    with open('counts.txt', 'r') as file:
        i = 0
        for line in file:
            # Split the line into two numbers
            yes_count, no_count = map(int, line.strip().split(';'))
            # Append the counts to the respective lists
            yes_counts[i] = yes_count
            no_counts[i] = no_count
# Flying Image Width
fi_width = 250
fi_height = 225

# Function to update counts and save to file
def update_counts(answer, qi):
    if answer == "yes":
        yes_counts[qi] += 1
    else:
        no_counts[qi] += 1
    
    with open(file_path, 'w') as file:
        for i in range(num_questions):
            file.write(f"{yes_counts[i]};{no_counts[i]}\n")


# Function to react the answer chosen
def react_answer(answer, qi):
    update_counts(answer, qi)
    match (answer, qi):
        case ("yes", 0):
            start_animation()
        case ("no", 0):
            update_question(1)
            show_question()
        case ("yes", 1):
            start_animation()
            update_question(0)
        case ("no", 1):
            start_animation()
            update_question(0)
        case _:
            start_animation()
            update_question(0)
    

# Function to start the animation of the Steinbock
def start_animation():
    # Hide the question and buttons
    question_label.place_forget()
    yes_button.place_forget()
    no_button.place_forget()

    # Show the Steinbock
    steinbock_label.pack()
    move_steinbock()

# Function to move the Steinbock across the screen
def move_steinbock():
    x = window.winfo_width()+100  # Start off-screen
    steinbock_label.place(x=x, y=200)

    def animate():
        nonlocal x
        if x > -fi_width:
            x -= 2  # Move right
            steinbock_label.place(x=x, y=window.winfo_height()//2-fi_height)
            window.after(3, animate)
        else:
        #     # After animation, show thanks message
        #     messagebox.showinfo("Animation", "Thanks!")
            steinbock_label.pack_forget()  # Hide the Steinbock
            show_question()  # Show the question again

    animate()

# Function to show the question and buttons again
def show_question():
    # Calculate the position for the question label
    width = window.winfo_screenwidth()
    height = window.winfo_screenheight()
    question_label.place(x=width/2, y=height/2-200, anchor='center')  # Centered and a bit up
    yes_button.place(x=width/2-150, y=height/2+50, anchor='center')
    no_button.place(x=width/2+150, y=height/2+50, anchor='center')

# Create the main window
window = tk.Tk()
window.title("Question")
window.attributes("-fullscreen", True)
window.configure(bg='yellow')

question_label = tk.Label(window, text=questions[0], bg='yellow', fg='purple', font=('Arial', 35))
yes_button = tk.Button(window, text="Ja", command=lambda: react_answer("yes", 0), font=('Arial', 24))
no_button = tk.Button(window, text="Nein", command=lambda: react_answer("no", 0), font=('Arial', 24))

# Question and buttons
def update_question(qi):
    question_label.config(text = questions[qi])
    yes_button.config(command=lambda: react_answer("yes", qi))
    no_button.config(command=lambda: react_answer("no", qi))

# Load and prepare the Steinbock image
steinbock_image = Image.open("steinbock-thanks.png")
steinbock_image = steinbock_image.resize((fi_width, fi_height), Image.LANCZOS)
steinbock_photo = ImageTk.PhotoImage(steinbock_image)

steinbock_label = tk.Label(window, image=steinbock_photo, bg='yellow')

# Start with the question displayed
update_question(0)
show_question()

# Start the GUI event loop
window.mainloop()
