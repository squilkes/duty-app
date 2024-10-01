import tkinter as tk
from tkinter import ttk
from tkinter import Spinbox
from ui.postman_window import open_add_postman_window, open_edit_postman_window
from ui.route_window import open_add_route_window, open_edit_route_window
from ui.select_postmen_window import open_select_postmen_window
from ui.duty_list_window import open_duty_list_window  # Import the duty list function
import db.database as database


class DutyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Duty Assignment App")

        # Initialize the database
        database.init_db()

        # Store selected postmen for the week
        self.selected_postmen = []

        # Configure grid layout for spacing and structure
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=1)

        # Add Week Label, Spinbox, and Select Postmen Button in the center
        week_frame = ttk.Frame(root)
        week_frame.grid(row=1, column=1, columnspan=2)

        self.week_label = ttk.Label(week_frame, text="Week:")
        self.week_label.grid(row=0, column=0, padx=5)

        self.week_spinbox = Spinbox(week_frame, from_=1, to=52, width=5)
        self.week_spinbox.grid(row=0, column=1, padx=5)

        self.select_postmen_button = ttk.Button(week_frame, text="Select Postmen", command=lambda: open_select_postmen_window(self.root, self.set_selected_postmen))
        self.select_postmen_button.grid(row=0, column=2, padx=5)

        # Add the "Generate Duty List" button centered below the week selector
        self.generate_duty_button = ttk.Button(root, text="Generate Duty List", command=self.generate_duty_list)
        self.generate_duty_button.grid(row=2, column=1, columnspan=2, pady=10)

        button_width = 15
        self.add_postman_button = ttk.Button(root, text="Add Postman", width=button_width, command=lambda: open_add_postman_window(self.root))
        self.add_postman_button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        self.edit_postman_button = ttk.Button(root, text="Edit Postman", width=button_width, command=lambda: open_edit_postman_window(self.root))
        self.edit_postman_button.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        self.add_route_button = ttk.Button(root, text="Add Route", width=button_width, command=lambda: open_add_route_window(self.root))
        self.add_route_button.grid(row=3, column=2, padx=10, pady=10, sticky="ew")

        self.edit_route_button = ttk.Button(root, text="Edit Routes", width=button_width, command=lambda: open_edit_route_window(self.root))
        self.edit_route_button.grid(row=3, column=3, padx=10, pady=10, sticky="ew")

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=1)

    def set_selected_postmen(self, postmen):
        """Store the selected postmen for the week."""
        self.selected_postmen = postmen

    def generate_duty_list(self):
        """Generate the duty list table based on the selected week and postmen."""
        week_number = int(self.week_spinbox.get())
        if not self.selected_postmen:
            print("No postmen selected for this week!")
            return
        open_duty_list_window(self.root, week_number, self.selected_postmen)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x400")
    app = DutyApp(root)
    root.mainloop()
