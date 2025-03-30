import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os
import time

# Path to the JSON file
DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "projects.json")

class DrawingProjectTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drawing Projects Tracker")
        self.projects = self.load_projects()
        self.tracking_projects = {}  # Dictionary to track multiple projects and their start times

        # UI Elements
        self.project_frame = tk.Frame(root)
        self.project_frame.pack(pady=10)

        self.add_button = tk.Button(root, text="Add Project", command=self.add_project)
        self.add_button.pack(pady=5)

        self.refresh_project_list()

    def load_projects(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as file:
                return json.load(file)
        return []

    def save_projects(self):
        with open(DATA_FILE, "w") as file:
            json.dump(self.projects, file, indent=4)
        self.refresh_project_list()  # Update the UI whenever the JSON file is saved

    def refresh_project_list(self):
        # Clear the frame
        for widget in self.project_frame.winfo_children():
            widget.destroy()

        # Add each project with Start/Pause, Edit, and Delete buttons
        for project in self.projects:
            project_row = tk.Frame(self.project_frame)
            project_row.pack(fill="x", pady=2)

            # Set the text color to green if the project is being tracked, otherwise black
            text_color = "green" if project["name"] in self.tracking_projects else "black"

            project_label = tk.Label(
                project_row,
                text=f"{project['name']} (Time: {self.format_time(project['time_spent'])})",
                width=40,
                anchor="w",
                fg=text_color  # Set the text color dynamically
            )
            project_label.pack(side="left", padx=5)

            # Start button with spacing
            toggle_button = tk.Button(
                project_row,
                text="▶",  # Unicode play icon
                width=3,
                height=1,
                command=lambda p=project: self.toggle_tracking(p)
            )
            toggle_button.pack(side="left", padx=(5, 20))  # Add spacing after the Start button

            # Edit button
            edit_button = tk.Button(
                project_row,
                text="✎",  # Unicode pencil icon
                width=3,
                height=1,
                command=lambda p=project: self.edit_project(p)
            )
            edit_button.pack(side="left", padx=5)

            # Delete button
            delete_button = tk.Button(
                project_row,
                text="🗑",  # Unicode trash can icon
                width=3,
                height=1,
                command=lambda p=project: self.delete_project(p)
            )
            delete_button.pack(side="left", padx=5)

            # Update button text if the project is being tracked
            if project["name"] in self.tracking_projects:
                toggle_button.config(text="⏸")  # Unicode pause icon

    def add_project(self):
        new_project_name = self.prompt_user("Enter new project name:")
        if new_project_name:
            self.projects.append({"name": new_project_name, "time_spent": 0})
            self.save_projects()

    def edit_project(self, project):
        new_name = self.prompt_user("Edit project name:", project["name"])
        if new_name:
            project["name"] = new_name
            self.save_projects()

    def delete_project(self, project):
        confirmation = self.prompt_user(f"Type the project name '{project['name']}' to confirm deletion:")
        if confirmation == project["name"]:
            if project["name"] in self.tracking_projects:
                del self.tracking_projects[project["name"]]  # Stop tracking if the project is deleted
            self.projects.remove(project)
            self.save_projects()
        else:
            messagebox.showerror("Error", "Project name does not match. Deletion canceled.")

    def toggle_tracking(self, project):
        project_name = project["name"]

        if project_name in self.tracking_projects:
            # Pause tracking
            elapsed_time = time.time() - self.tracking_projects[project_name]
            project["time_spent"] += int(elapsed_time)  # Store time in seconds
            del self.tracking_projects[project_name]
            self.save_projects()
        else:
            # Start tracking
            self.tracking_projects[project_name] = time.time()

        self.refresh_project_list()  # Ensure the UI is updated for button text and time

    def format_time(self, seconds):
        """Convert seconds to HH:MM:SS format."""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

    def prompt_user(self, prompt, default_value=""):
        return simpledialog.askstring("Input", prompt, initialvalue=default_value)

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingProjectTrackerApp(root)
    root.mainloop()