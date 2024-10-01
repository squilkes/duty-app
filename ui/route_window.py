import tkinter as tk
from tkinter import ttk
import db.database as database
from utils import center_window_on_parent

def open_add_route_window(parent):
    new_window = tk.Toplevel(parent)
    new_window.title("Add Route")
    center_window_on_parent(parent, new_window)

    ttk.Label(new_window, text="Enter Route Name:").grid(row=0, column=0, padx=10, pady=5)
    route_name_entry = ttk.Entry(new_window)
    route_name_entry.grid(row=0, column=1, padx=10, pady=5)

    ttk.Button(new_window, text="Submit", command=lambda: submit_route(route_name_entry.get(), new_window)).grid(row=1, column=0, columnspan=2, pady=10)

def submit_route(route_name, window):
    if route_name:
        database.add_route(route_name)
        print(f"Route '{route_name}' added.")
    window.destroy()

def open_edit_route_window(parent):
    new_window = tk.Toplevel(parent)
    new_window.title("Edit or Delete Routes")
    center_window_on_parent(parent, new_window)

    routes = database.get_all_routes()
    for i, route in enumerate(routes):
        ttk.Label(new_window, text=route[1]).grid(row=i, column=0, padx=10, pady=5)
        ttk.Button(new_window, text="Edit", command=lambda r=route: open_edit_route_form(parent, r)).grid(row=i, column=1, padx=5, pady=5)
        ttk.Button(new_window, text="Delete", command=lambda r=route: delete_route(r[0], new_window)).grid(row=i, column=2, padx=5, pady=5)

def open_edit_route_form(parent, route):
    route_id, route_name = route
    new_window = tk.Toplevel(parent)
    new_window.title(f"Edit Route: {route_name}")
    center_window_on_parent(parent, new_window)

    ttk.Label(new_window, text="Edit Route Name:").grid(row=0, column=0, padx=10, pady=5)
    route_name_entry = ttk.Entry(new_window)
    route_name_entry.insert(0, route_name)
    route_name_entry.grid(row=0, column=1, padx=10, pady=5)

    ttk.Button(new_window, text="Save Changes", command=lambda: save_route_changes(route_id, route_name_entry.get(), new_window)).grid(row=1, column=0, padx=5, pady=10)
    ttk.Button(new_window, text="Cancel", command=new_window.destroy).grid(row=1, column=1, padx=5, pady=10)

def save_route_changes(route_id, route_name, window):
    if route_name:
        database.update_route_name(route_id, route_name)
        print(f"Route '{route_name}' updated.")
    window.destroy()

def delete_route(route_id, window):
    database.delete_route(route_id)
    print(f"Route with ID {route_id} deleted.")
    window.destroy()
