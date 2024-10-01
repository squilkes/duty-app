import tkinter as tk
from tkinter import ttk
import db.database as database
from utils import center_window_on_parent

def open_duty_list_window(parent, week_number, selected_postmen):
    """Opens a new window showing the duty list table."""
    new_window = tk.Toplevel(parent)
    new_window.title(f"Duty List for Week {week_number}")

    # Define days of the week
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    # Get all routes (duties) from the database
    routes = database.get_all_routes()

    # Create a table header with the days of the week
    for col, day in enumerate(days_of_week, start=1):
        header = ttk.Label(new_window, text=day, font=("Arial", 10, "bold"))
        header.grid(row=0, column=col, padx=10, pady=5)

    # Function to get the rotating day off for a postman
    def get_day_off(postman_index):
        return (postman_index + week_number - 1) % 6  # Rotating days off, Monday = 0, ..., Saturday = 5

    # Create the table rows for each route (duty)
    for row, route in enumerate(routes, start=1):
        route_label = ttk.Label(new_window, text=route[1], font=("Arial", 10))
        route_label.grid(row=row, column=0, padx=10, pady=5, sticky="w")

        # Assign postmen to each day, skipping their rotating day off
        for col, day in enumerate(days_of_week, start=1):
            # Find a postman who can work on this day
            for i, postman in enumerate(selected_postmen):
                if database.postman_knows_route(postman[0], route[0]) and get_day_off(i) != (col - 1):
                    postman_label = ttk.Label(new_window, text=postman[1], font=("Arial", 10))
                    postman_label.grid(row=row, column=col, padx=10, pady=5)
                    break

    # Center the window
    center_window_on_parent(parent, new_window)
