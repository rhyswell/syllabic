"""
gui.py

Tkinter interface for Syllabic.
Select week → Generate assignments.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from app import SyllabicEngine


class SyllabicGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Syllabic - AI Assignment Generator")
        self.root.geometry("400x200")

        self.engine = SyllabicEngine()

        self.create_widgets()

    def create_widgets(self):

        title_label = tk.Label(
            self.root,
            text="Syllabic",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)

        week_label = tk.Label(self.root, text="Select Week:")
        week_label.pack()

        self.week_var = tk.StringVar()

        self.week_dropdown = ttk.Combobox(
            self.root,
            textvariable=self.week_var,
            state="readonly"
        )

        self.week_dropdown["values"] = [str(i) for i in range(1, 15)]
        self.week_dropdown.current(0)
        self.week_dropdown.pack(pady=5)

        generate_button = tk.Button(
            self.root,
            text="Generate Assignments",
            command=self.generate_assignments
        )
        generate_button.pack(pady=20)

    def generate_assignments(self):

        try:
            week_number = int(self.week_var.get())

            messagebox.showinfo(
                "Processing",
                f"Generating assignments for Week {week_number}..."
            )

            self.engine.generate_for_week(week_number)

            messagebox.showinfo(
                "Success",
                f"Assignments for Week {week_number} generated successfully!"
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"An error occurred:\n{str(e)}"
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = SyllabicGUI(root)
    root.mainloop()
