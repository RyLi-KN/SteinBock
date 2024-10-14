import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time
import os

# Initialize counts
yes_count = 0
no_count = 0

# File to store counts
file_path = "counts.txt"

# Flying Image Width
fi_width = 225
fi_height = 200

# Load counts from the file if it exists
if os.path.exists(file_path):
    with open(file_path, 'r') as file:
        yes_count = int(file.readline().strip())
        no_count = int(file.readline().strip())

# Function to update counts and save to file
def update_counts(answer):
    global yes_count, no_count
    if answer == "yes":
        yes_count += 1
    else:
        no_count += 1
    
    with open(file_path, 'w') as file:
        file.write(f"{yes_count}\n{no_count}\n")

    start_animation()

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
            x -= 4  # Move right
            steinbock_label.place(x=x, y=window.winfo_height()//2-fi_height)
            window.after(8, animate)
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
    yes_button.place(x=width/2-100, y=height/2+50, anchor='center')
    no_button.place(x=width/2+100, y=height/2+50, anchor='center')

# Create the main window
window = tk.Tk()
window.title("Question")
window.attributes("-fullscreen", True)
window.configure(bg='yellow')

# Question and buttons
question_label = tk.Label(window, text="Do you like Python?", bg='yellow', fg='purple', font=('Arial', 24))
yes_button = tk.Button(window, text="Yes", command=lambda: update_counts("yes"), font=('Arial', 18))
no_button = tk.Button(window, text="No", command=lambda: update_counts("no"), font=('Arial', 18))

# Load and prepare the Steinbock image
steinbock_image = Image.open("steinbock-thanks.png")
steinbock_image = steinbock_image.resize((fi_width, fi_height), Image.LANCZOS)
steinbock_photo = ImageTk.PhotoImage(steinbock_image)

steinbock_label = tk.Label(window, image=steinbock_photo, bg='yellow')

# Start with the question displayed
show_question()

# Start the GUI event loop
window.mainloop()
