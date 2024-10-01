import tkinter as tk
from tkinter import ttk
import db.database as database
from utils import center_window_on_parent

def open_add_postman_window(parent):
    new_window = tk.Toplevel(parent)
    new_window.title("Add Postman")
    center_window_on_parent(parent, new_window)

    # Postman name field
    ttk.Label(new_window, text="Enter Postman Name:").grid(row=0, column=0, padx=10, pady=5)
    postman_name_entry = ttk.Entry(new_window)
    postman_name_entry.grid(row=0, column=1, padx=10, pady=5)

    routes = database.get_all_routes()
    checkboxes = []
    for i, route in enumerate(routes):
        var = tk.IntVar()
        checkbox = ttk.Checkbutton(new_window, text=route[1], variable=var)
        checkbox.grid(row=i + 1, column=0, padx=10, pady=2, sticky=tk.W)
        checkboxes.append((route[0], var))

    ttk.Button(new_window, text="Submit", command=lambda: submit_postman(postman_name_entry.get(), checkboxes, new_window)).grid(row=len(routes) + 1, column=0, columnspan=2, pady=10)

    # Let the window size itself to fit the contents
    new_window.update_idletasks()
    new_window.geometry("")  # Set an empty geometry to let it fit content

def submit_postman(postman_name, checkboxes, window):
    if postman_name:
        postman_id = database.add_postman(postman_name)
        for route_id, var in checkboxes:
            if var.get() == 1:
                database.assign_route_to_postman(postman_id, route_id)
        print(f"Postman '{postman_name}' added.")
    window.destroy()

def open_edit_postman_window(parent):
    new_window = tk.Toplevel(parent)
    new_window.title("Edit or Delete Postmen")
    center_window_on_parent(parent, new_window)

    postmen = database.get_all_postmen()
    for i, postman in enumerate(postmen):
        ttk.Label(new_window, text=postman[1]).grid(row=i, column=0, padx=10, pady=5)
        ttk.Button(new_window, text="Edit", command=lambda p=postman: open_edit_postman_form(parent, p)).grid(row=i, column=1, padx=5, pady=5)
        ttk.Button(new_window, text="Delete", command=lambda p=postman: delete_postman(p[0], new_window)).grid(row=i, column=2, padx=5, pady=5)

def open_edit_postman_form(parent, postman):
    postman_id, postman_name = postman
    new_window = tk.Toplevel(parent)
    new_window.title(f"Edit Postman: {postman_name}")
    center_window_on_parent(parent, new_window)

    ttk.Label(new_window, text="Edit Postman Name:").grid(row=0, column=0, padx=10, pady=5)
    postman_name_entry = ttk.Entry(new_window)
    postman_name_entry.insert(0, postman_name)
    postman_name_entry.grid(row=0, column=1, padx=10, pady=5)

    routes = database.get_all_routes()
    known_routes = database.get_postman_routes(postman_id)
    checkboxes = []
    for i, route in enumerate(routes):
        var = tk.IntVar(value=1 if route[0] in known_routes else 0)
        checkbox = ttk.Checkbutton(new_window, text=route[1], variable=var)
        checkbox.grid(row=i + 1, column=0, padx=10, pady=2, sticky=tk.W)
        checkboxes.append((route[0], var))

    ttk.Button(new_window, text="Save Changes", command=lambda: save_postman_changes(postman_id, postman_name_entry.get(), checkboxes, new_window)).grid(row=len(routes) + 1, column=0, columnspan=2, pady=10)
    ttk.Button(new_window, text="Cancel", command=new_window.destroy).grid(row=len(routes) + 1, column=1, padx=5, pady=10)

def save_postman_changes(postman_id, postman_name, checkboxes, window):
    if postman_name:
        database.update_postman_name(postman_id, postman_name)
        database.clear_postman_routes(postman_id)
        for route_id, var in checkboxes:
            if var.get() == 1:
                database.assign_route_to_postman(postman_id, route_id)
        print(f"Postman '{postman_name}' updated.")
    window.destroy()

def delete_postman(postman_id, window):
    database.delete_postman(postman_id)
    print(f"Postman with ID {postman_id} deleted.")
    window.destroy()