import tkinter as tk
from ui.main_window import DutyApp

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("640x360")
    app = DutyApp(root)
    root.mainloop()
