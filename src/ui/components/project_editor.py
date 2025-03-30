from tkinter import Tk, Label, Entry, Button, StringVar, messagebox
import json
import os

class ProjectEditor:
    def __init__(self, master, project=None, on_save=None):
        self.master = master
        self.on_save = on_save
        self.project = project

        self.name_var = StringVar()
        self.time_var = StringVar()

        self.setup_ui()

        if project:
            self.name_var.set(project['name'])
            self.time_var.set(project['time_spent'])

    def setup_ui(self):
        Label(self.master, text="Project Name:").grid(row=0, column=0)
        Entry(self.master, textvariable=self.name_var).grid(row=0, column=1)

        Label(self.master, text="Time Spent (hours):").grid(row=1, column=0)
        Entry(self.master, textvariable=self.time_var).grid(row=1, column=1)

        Button(self.master, text="Save", command=self.save_project).grid(row=2, column=0, columnspan=2)
        Button(self.master, text="Delete", command=self.delete_project).grid(row=3, column=0, columnspan=2)

    def save_project(self):
        name = self.name_var.get()
        time_spent = self.time_var.get()

        if not name:
            messagebox.showerror("Error", "Project name cannot be empty.")
            return

        if not time_spent.isdigit():
            messagebox.showerror("Error", "Time spent must be a number.")
            return

        project_data = {
            'name': name,
            'time_spent': int(time_spent)
        }

        if self.on_save:
            self.on_save(project_data)

        messagebox.showinfo("Success", "Project saved successfully.")

    def delete_project(self):
        if self.on_save and self.project:
            self.on_save(None)
            messagebox.showinfo("Success", "Project deleted successfully.")