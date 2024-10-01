import tkinter as tk
from tkinter import ttk
import db.database as database
from utils import center_window_on_parent

def open_select_postmen_window(parent, set_selected_postmen):
    """Opens a window to select postmen for the week."""
    new_window = tk.Toplevel(parent)
    new_window.title("Select Postmen")
    center_window_on_parent(parent, new_window)

    # Fetch all postmen from the database
    postmen = database.get_all_postmen()

    # List of postmen with checkboxes
    checkboxes = []

    # Add the "Select All" checkbox
    select_all_var = tk.IntVar()

    def toggle_select_all():
        """Toggle all checkboxes based on the Select All checkbox."""
        for _, var in checkboxes:
            var.set(select_all_var.get())

    select_all_checkbox = ttk.Checkbutton(new_window, text="Select All", variable=select_all_var, command=toggle_select_all)
    select_all_checkbox.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

    # List of postmen with individual checkboxes
    for i, postman in enumerate(postmen, start=1):
        var = tk.IntVar()
        checkbox = ttk.Checkbutton(new_window, text=postman[1], variable=var)
        checkbox.grid(row=i, column=0, padx=10, pady=2, sticky=tk.W)
        checkboxes.append((postman, var))  # Store (postman, IntVar) for future reference

    def submit_postmen():
        """Submit selected postmen and pass them to the main app."""
        selected_postmen = [postman for postman, var in checkboxes if var.get() == 1]
        set_selected_postmen(selected_postmen)  # Pass the selected postmen to the main app
        new_window.destroy()

    submit_button = ttk.Button(new_window, text="Submit", command=submit_postmen)
    submit_button.grid(row=len(postmen) + 1, column=0, pady=10)

    # Center the window
    center_window_on_parent(parent, new_window)
