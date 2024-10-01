def center_window_on_parent(parent, window, min_width=600, min_height=300):
    # Set the minimum size for the window
    window.minsize(min_width, min_height)

    # Let the window dynamically size based on its content
    window.update_idletasks()  # Update window size based on content

    # Get the parent window's position and size
    parent_x = parent.winfo_rootx()
    parent_y = parent.winfo_rooty()
    parent_width = parent.winfo_width()
    parent_height = parent.winfo_height()

    # Get the new window's current size after dynamic sizing
    window_width = max(window.winfo_width(), min_width)
    window_height = max(window.winfo_height(), min_height)

    # Calculate the position to center the window on the parent window
    x = parent_x + (parent_width // 2) - (window_width // 2)
    y = parent_y + (parent_height // 2) - (window_height // 2)

    # Set the geometry for the window, without forcing the size
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")
