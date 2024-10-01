import tkinter as tk
from tkinter import ttk
import database

class DutyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Duty Assignment App")

        # Initialize the database
        database.init_db()

        # Add Postman Button
        self.add_postman_button = ttk.Button(root, text="Add Postman", command=self.open_add_postman_window)
        self.add_postman_button.grid(row=0, column=0, padx=10, pady=10)

        # Edit Postman Button
        self.edit_postman_button = ttk.Button(root, text="Edit Postman", command=self.open_edit_postman_window)
        self.edit_postman_button.grid(row=2, column=0, padx=10, pady=10)

        # Add Route Button
        self.add_route_button = ttk.Button(root, text="Add Route", command=self.open_add_route_window)
        self.add_route_button.grid(row=1, column=0, padx=10, pady=10)

        # Edit Routes Button
        self.edit_route_button = ttk.Button(root, text="Edit Routes", command=self.open_edit_route_window)
        self.edit_route_button.grid(row=3, column=0, padx=10, pady=10)

    def center_window_on_parent(self, parent, window, width=300, height=200):
        # Get the parent window's position and size
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        # Calculate the position to center the pop-up on the parent window
        x = parent_x + (parent_width // 2) - (width // 2)
        y = parent_y + (parent_height // 2) - (height // 2)

        # Set the geometry for the new window
        window.geometry(f"{width}x{height}+{x}+{y}")

    def open_add_postman_window(self):
        # Create a new window (Toplevel)
        new_window = tk.Toplevel(self.root)
        new_window.title("Add Postman")

        # Call the utility function to center the window
        self.center_window_on_parent(self.root, new_window, width=300, height=200)

        # Postman name field
        ttk.Label(new_window, text="Enter Postman Name:").grid(row=0, column=0, padx=10, pady=5)
        postman_name_entry = ttk.Entry(new_window)
        postman_name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Get all routes from the database
        routes = database.get_all_routes()

        # List to hold checkbox variables
        checkboxes = []
        for i, route in enumerate(routes):
            var = tk.IntVar()  # Variable to track checkbox state (1 for checked, 0 for unchecked)
            checkbox = ttk.Checkbutton(new_window, text=route[1], variable=var)  # route[1] is the route name
            checkbox.grid(row=i + 1, column=0, padx=10, pady=2, sticky=tk.W)
            checkboxes.append((route[0], var))  # Store route ID and the variable

        # Submit button
        ttk.Button(new_window, text="Submit", command=lambda: self.submit_postman(postman_name_entry.get(), checkboxes, new_window)).grid(row=len(routes) + 1, column=0, columnspan=2, pady=10)

    def submit_postman(self, postman_name, checkboxes, window):
        if postman_name:
            # Add the postman to the database
            postman_id = database.add_postman(postman_name)

            # Assign selected routes to the postman
            for route_id, var in checkboxes:
                if var.get() == 1:  # Checkbox is checked
                    database.assign_route_to_postman(postman_id, route_id)

            print(f"Postman '{postman_name}' added with selected routes.")
        window.destroy()  # Close the window after submission

    def open_add_route_window(self):
        # Create a new window (Toplevel)
        new_window = tk.Toplevel(self.root)
        new_window.title("Add Route")

        # Call the utility function to center the window
        self.center_window_on_parent(self.root, new_window, width=300, height=200)

        # Route name field
        ttk.Label(new_window, text="Enter Route Name:").grid(row=0, column=0, padx=10, pady=5)
        route_name_entry = ttk.Entry(new_window)
        route_name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Submit button
        ttk.Button(new_window, text="Submit", command=lambda: self.submit_route(route_name_entry.get(), new_window)).grid(row=1, column=0, columnspan=2, pady=10)

    def submit_route(self, route_name, window):
        if route_name:
            # Add the route to the database
            database.add_route(route_name)
            print(f"Route '{route_name}' added.")
        window.destroy()  # Close the window after submission


    def open_edit_postman_window(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Edit or Delete Postmen")

        # Call the utility function to center the window
        self.center_window_on_parent(self.root, new_window, width=300, height=200)

        # Fetch all postmen from the database
        postmen = database.get_all_postmen()

        # Display each postman with Edit and Delete buttons
        for i, postman in enumerate(postmen):
            ttk.Label(new_window, text=postman[1]).grid(row=i, column=0, padx=10, pady=5)
            # Edit button
            ttk.Button(new_window, text="Edit", command=lambda p=postman: self.open_edit_postman_form(p)).grid(row=i, column=1, padx=5, pady=5)
            # Delete button
            ttk.Button(new_window, text="Delete", command=lambda p=postman: self.delete_postman(p[0], new_window)).grid(row=i, column=2, padx=5, pady=5)

    def open_edit_postman_form(self, postman):
        postman_id, postman_name = postman
        new_window = tk.Toplevel(self.root)
        new_window.title(f"Edit Postman: {postman_name}")

        # Call the utility function to center the window
        self.center_window_on_parent(self.root, new_window, width=300, height=200)

        # Postman name field pre-filled
        ttk.Label(new_window, text="Edit Postman Name:").grid(row=0, column=0, padx=10, pady=5)
        postman_name_entry = ttk.Entry(new_window)
        postman_name_entry.insert(0, postman_name)  # Pre-fill the name
        postman_name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Get all routes from the database
        routes = database.get_all_routes()
        known_routes = database.get_postman_routes(postman_id)  # Get routes the postman knows

        # List to hold checkbox variables
        checkboxes = []
        for i, route in enumerate(routes):
            var = tk.IntVar(value=1 if route[0] in known_routes else 0)  # Pre-select known routes
            checkbox = ttk.Checkbutton(new_window, text=route[1], variable=var)
            checkbox.grid(row=i + 1, column=0, padx=10, pady=2, sticky=tk.W)
            checkboxes.append((route[0], var))

        # Save button
        ttk.Button(new_window, text="Save Changes", command=lambda: self.save_postman_changes(postman_id, postman_name_entry.get(), checkboxes, new_window)).grid(row=len(routes) + 1, column=0, columnspan=2, pady=10)

        # Cancel button (to discard changes)
        ttk.Button(new_window, text="Cancel", command=new_window.destroy).grid(row=len(routes) + 1, column=1, padx=5, pady=30)

    def save_postman_changes(self, postman_id, postman_name, checkboxes, window):
        if postman_name:
            # Update postman name in the database
            database.update_postman_name(postman_id, postman_name)

            # Update postman routes in the database
            database.clear_postman_routes(postman_id)  # Clear all routes
            for route_id, var in checkboxes:
                if var.get() == 1:  # Checkbox is checked
                    database.assign_route_to_postman(postman_id, route_id)

            print(f"Postman '{postman_name}' updated.")
        window.destroy()

    def delete_postman(self, postman_id, window):
        # Delete the postman from the database
        database.delete_postman(postman_id)
        print(f"Postman with ID {postman_id} deleted.")
        window.destroy()  # Close the window and refresh

    def open_edit_route_window(self):
        # Create a new window to list and edit routes
        new_window = tk.Toplevel(self.root)
        new_window.title("Edit or Delete Routes")

        # Call the utility function to center the window
        self.center_window_on_parent(self.root, new_window, width=300, height=200)

        # Get all routes from the database
        routes = database.get_all_routes()

        # List all routes with Edit and Delete buttons
        for i, route in enumerate(routes):
            ttk.Label(new_window, text=route[1]).grid(row=i, column=0, padx=10, pady=5)
            # Edit button for each route
            ttk.Button(new_window, text="Edit", command=lambda r=route: self.open_edit_route_form(r)).grid(row=i, column=1, padx=5, pady=5)
            # Delete button for each route
            ttk.Button(new_window, text="Delete", command=lambda r=route: self.delete_route(r[0], new_window)).grid(row=i, column=2, padx=5, pady=5)

    def open_edit_route_form(self, route):
        route_id, route_name = route
        new_window = tk.Toplevel(self.root)
        new_window.title(f"Edit Route: {route_name}")

        # Call the utility function to center the window
        self.center_window_on_parent(self.root, new_window, width=300, height=200)

        # Route name field pre-filled
        ttk.Label(new_window, text="Edit Route Name:").grid(row=0, column=0, padx=10, pady=5)
        route_name_entry = ttk.Entry(new_window)
        route_name_entry.insert(0, route_name)
        route_name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Save Changes button
        ttk.Button(new_window, text="Save Changes", command=lambda: self.save_route_changes(route_id, route_name_entry.get(), new_window)).grid(row=1, column=0, padx=5, pady=10)
        # Cancel button
        ttk.Button(new_window, text="Cancel", command=new_window.destroy).grid(row=1, column=1, padx=5, pady=10)

    def save_route_changes(self, route_id, route_name, window):
        if route_name:
            # Update route name in the database
            database.update_route_name(route_id, route_name)
            print(f"Route '{route_name}' updated.")
        window.destroy()

    def delete_route(self, route_id, window):
        # Delete the route from the database
        database.delete_route(route_id)
        print(f"Route with ID {route_id} deleted.")
        window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("640x360")
    app = DutyApp(root)
    root.mainloop()
