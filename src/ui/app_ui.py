from tkinter import Tk, Frame, Listbox, Button, Entry, Label, END, messagebox
from .components.project_list import ProjectList
from components.project_editor import ProjectEditor
import json

class AppUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Drawing Project Tracker")
        self.master.geometry("400x400")

        self.project_list_frame = Frame(self.master)
        self.project_list_frame.pack(side="left", fill="both", expand=True)

        self.project_editor_frame = Frame(self.master)
        self.project_editor_frame.pack(side="right", fill="both", expand=True)

        self.project_list = ProjectList(self.project_list_frame)
        self.project_editor = ProjectEditor(self.project_editor_frame, self.project_list)

        self.load_projects()

    def load_projects(self):
        try:
            with open('src/data/projects.json', 'r') as file:
                projects = json.load(file)
                self.project_list.refresh(projects)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load projects: {e}")

if __name__ == "__main__":
    root = Tk()
    app = AppUI(root)
    root.mainloop()