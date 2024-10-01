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

    # Debugging: Check if selected postmen are being passed correctly
    print(f"Selected Postmen for Week {week_number}: {[postman[1] for postman in selected_postmen]}")

    # Create a table header with the days of the week
    for col, day in enumerate(days_of_week, start=1):
        header = ttk.Label(new_window, text=day, font=("Arial", 10, "bold"))
        header.grid(row=0, column=col, padx=10, pady=5)

    # Function to get the rotating day off for a postman
    def get_day_off(postman_index):
        return (postman_index + week_number - 1) % 6  # Rotating days off, Monday = 0, ..., Saturday = 5

    # Track assigned postmen for each day
    assigned_postmen_per_day = {day: set() for day in days_of_week}

    # Create the table rows for each route (duty)
    for row, route in enumerate(routes, start=1):
        route_label = ttk.Label(new_window, text=route[1], font=("Arial", 10))
        route_label.grid(row=row, column=0, padx=10, pady=5, sticky="w")

        # Assign postmen to each day, skipping their rotating day off
        for col, day in enumerate(days_of_week, start=1):
            # Find a postman who can work on this day and hasn't been assigned to another route yet
            for i, postman in enumerate(selected_postmen):
                knows_route = database.postman_knows_route(postman[0], route[0])
                day_off = get_day_off(i)

                # Ensure the postman knows the route, it's not their day off, and they aren't assigned to another route
                if knows_route and day_off != (col - 1) and postman[1] not in assigned_postmen_per_day[day]:
                    postman_label = ttk.Label(new_window, text=postman[1], font=("Arial", 10))
                    postman_label.grid(row=row, column=col, padx=10, pady=5)
                    print(f"Assigned {postman[1]} to {route[1]} on {day}")

                    # Mark this postman as assigned for this day
                    assigned_postmen_per_day[day].add(postman[1])
                    break

    # Center the window
    center_window_on_parent(parent, new_window)


