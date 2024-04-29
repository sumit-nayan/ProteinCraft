import os
import subprocess
import tkinter as tk
from tkinter import ttk
from protein_generator import generate_protein_data
import time
import threading

def open_folder():
    output_folder = os.path.join(os.getcwd(), "Result")
    if os.name == 'nt':
        subprocess.Popen(['explorer', output_folder])
    elif os.name == 'posix':
        subprocess.Popen(['xdg-open', output_folder])

def update_timer():
    current_time = time.time() - start_time
    timer_label.configure(text=f"Time elapsed: {current_time:.2f} seconds")
    if not result_displayed:
        root.after(100, update_timer)


def generate_protein_data_gui():
    global start_time, result_displayed
    start_time = time.time()  # Start the timer
    result_displayed = False
    update_timer()  # Start updating the timer
    num_lines = int(num_lines_var.get())
    exclude_aa = exclude_aa_var.get()
    num_models = int(num_models_var.get())
    exclude_aa = [char.upper() for char in exclude_aa if char.isalpha()]

    threading.Thread(target=generate_protein_data_and_update_gui, args=(num_lines, exclude_aa, num_models)).start()

def generate_protein_data_and_update_gui(num_lines, exclude_aa, num_models):
    global start_time, result_displayed
    zip_filename = generate_protein_data(num_lines, exclude_aa, num_models)
    open_button.configure(state=tk.NORMAL)
    elapsed_time = time.time() - start_time  # Calculate elapsed time
    info_label.configure(text=f"File Name: {zip_filename}\nNumber of pdb files in zip: {num_models}\nNumber of Models: {num_models}\nTime taken: {elapsed_time:.2f} seconds")
    result_displayed = True

# GUI
root = tk.Tk()
root.title("BT 305 Project")

# Get display size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set window size to 60% of display size
window_width = int(0.7 * screen_width)
window_height = int(0.9 * screen_height)

root.geometry(f"{window_width}x{window_height}")

# Calculate font and widget size based on window size
font_size = int(window_height / 33)  # Adjust as needed

# Customize the style
style = ttk.Style()
style.theme_use('clam')  # Choose a modern theme (e.g., clam)
style.configure('TButton', font=('Arial', font_size))  # Customize button font
style.configure('TEntry', font=('Arial', font_size))  # Customize entry font
style.configure('Red.TLabel', foreground='red')  # Customize label font color to red

mainframe = ttk.Frame(root, padding="20")
mainframe.grid(column=0, row=0, sticky=(tk.W, tk.N, tk.E, tk.S))

# Heading
heading_label = ttk.Label(mainframe, text="BT 305 Project", font=('Arial', font_size * 2))
heading_label.grid(column=0, row=0, columnspan=2, sticky=tk.W)

# Create a StringVar to hold the value of the entry fields
num_lines_var = tk.StringVar()
exclude_aa_var = tk.StringVar()
num_models_var = tk.StringVar()

# Validation function to allow only numeric input for Number of Lines
def validate_numeric_input(new_value):
    if new_value.isdigit() or new_value == "":
        return True
    else:
        root.bell()  # Produce a system beep
        root.after(100, clear_alert)  # Clear the alert after 100 milliseconds
        return False

# Validation function to allow only alphabetic characters without spaces for Exclude Amino Acids
def validate_alpha_input(new_value):
    if new_value.isalpha() or new_value == "":
        return True
    else:
        root.bell()  # Produce a system beep
        root.after(100, clear_alert)  # Clear the alert after 100 milliseconds
        return False

# Validation command to link the validation functions to the entry fields
validate_numeric_cmd = root.register(validate_numeric_input)
validate_alpha_cmd = root.register(validate_alpha_input)

# Create the entry fields with validation
ttk.Label(mainframe, text="Number of Sequences:", font=('Arial', font_size)).grid(column=0, row=1, sticky=tk.W)
num_lines_entry = ttk.Entry(mainframe, textvariable=num_lines_var, font=('Arial', font_size), validate="key", validatecommand=(validate_numeric_cmd, "%P"))
num_lines_entry.grid(column=1, row=1, sticky=tk.W+tk.E)  # Adjust size with window

ttk.Label(mainframe, text="Exclude Amino Acids:", font=('Arial', font_size)).grid(column=0, row=2, sticky=tk.W)
exclude_aa_entry = ttk.Entry(mainframe, textvariable=exclude_aa_var, font=('Arial', font_size), validate="key", validatecommand=(validate_alpha_cmd, "%P"))
exclude_aa_entry.grid(column=1, row=2, sticky=tk.W+tk.E)  # Adjust size with window

ttk.Label(mainframe, text="Number of Models:", font=('Arial', font_size)).grid(column=0, row=3, sticky=tk.W)
num_models_entry = ttk.Entry(mainframe, textvariable=num_models_var, font=('Arial', font_size), validate="key", validatecommand=(validate_numeric_cmd, "%P"))
num_models_entry.grid(column=1, row=3, sticky=tk.W+tk.E)  # Adjust size with window

# Function to clear the alert
def clear_alert():
    num_lines_entry.configure(style='TEntry')  # Reset the style to default

generate_button = ttk.Button(mainframe, text="Generate", command=generate_protein_data_gui)
generate_button.grid(column=1, row=4, sticky=tk.E)  # Align button to the right

# Additional line below Generate button
font_size2 = font_size - 4
additional_label = ttk.Label(mainframe, text="(Don't forget to note down the output protein zip file name of current iteration)\n Click on Open Folder buttom to open the folder containing zip file", font=('Arial', font_size2), style='Red.TLabel')
additional_label.grid(column=0, row=5, columnspan=2, sticky=tk.W)

open_button = ttk.Button(mainframe, text="Open Folder", command=open_folder, state=tk.DISABLED)
open_button.grid(column=1, row=6, sticky=tk.E)  # Align button to the right

info_label = ttk.Label(mainframe, text="", font=('Arial', font_size))
info_label.grid(column=0, row=7, columnspan=2, sticky=tk.W)

timer_label = ttk.Label(mainframe, text="Time elapsed: 0.00 seconds", font=('Arial', font_size))
timer_label.grid(column=0, row=8, columnspan=2, sticky=tk.W)

# Footer
footer_label = ttk.Label(mainframe, text="Made by:\nSumit Nayan (210106077)", font=('Arial', font_size2-7))
footer_label.grid(column=0, row=9, columnspan=2, sticky=tk.E)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.mainloop()
