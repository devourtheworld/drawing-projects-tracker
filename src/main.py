import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os
import time
import datetime  # Add this import for date and time handling

# Path to the JSON file
DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "projects.json")

class DrawingProjectTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drawing Projects Tracker")
        
        # Set fixed window size
        self.root.geometry("500x400")  # Width x Height
        # self.root.resizable(False, False)  # Disable resizing

        self.current_file = None  # Track the currently loaded file
        self.projects = self.load_projects()
        self.tracking_projects = {}  # Dictionary to track multiple projects and their start times

        # Menu Bar
        menu_bar = tk.Menu(root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Load Custom File", command=self.load_custom_file)
        menu_bar.add_cascade(label="File", menu=file_menu)
        root.config(menu=menu_bar)

        # Project Counter Label
        self.project_counter_label = tk.Label(root, text=f"Total Projects: {len(self.projects)}", font=("Arial", 12))
        self.project_counter_label.pack(pady=5)

        # UI Elements
        self.project_frame = tk.Frame(root)
        self.project_frame.pack(pady=10)

        self.add_button = tk.Button(root, text="Add Project", command=self.add_project)
        self.add_button.pack(pady=5)

        self.refresh_project_list()

    def load_projects(self):
        # Load the configuration file
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
        if os.path.exists(config_path):
            with open(config_path, "r") as config_file:
                config = json.load(config_file)
                custom_file = config.get("last_loaded_file")
        else:
            custom_file = None

        # Try to load the custom file if it exists
        if custom_file and os.path.exists(custom_file):
            self.current_file = custom_file
        else:
            # Fall back to the default file
            self.current_file = DATA_FILE

        # Load the projects from the selected file
        if os.path.exists(self.current_file):
            with open(self.current_file, "r") as file:
                try:
                    projects = json.load(file)
                    # Add default values for missing fields
                    for project in projects:
                        if "created_at" not in project:
                            project["created_at"] = "Unknown"
                        if "last_tracked" not in project:
                            project["last_tracked"] = "Never"
                    return projects
                except json.JSONDecodeError:
                    messagebox.showerror("Error", "Invalid JSON format in the file.")
                    return []
        else:
            messagebox.showerror("Error", f"File not found: {self.current_file}")
            return []

    def save_projects(self):
        if self.current_file:
            with open(self.current_file, "w") as file:
                json.dump(self.projects, file, indent=4)
            self.refresh_project_list()  # Update the UI whenever the JSON file is saved
        else:
            messagebox.showerror("Error", "No file selected to save projects.")

    def refresh_project_list(self):
        # Clear the frame
        for widget in self.project_frame.winfo_children():
            widget.destroy()

        # Update the project counter
        self.project_counter_label.config(text=f": {len(self.projects)}")

        # Add each project with Start/Pause, Edit, Delete, and Details buttons
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

            # Details button
            details_button = tk.Button(
                project_row,
                text="Details",
                width=6,
                height=1,
                command=lambda p=project: self.show_project_details(p)
            )
            details_button.pack(side="left", padx=5)

            # Update button text if the project is being tracked
            if project["name"] in self.tracking_projects:
                toggle_button.config(text="⏸")  # Unicode pause icon

    def add_project(self):
        new_project_name = self.prompt_user("Enter new project name:")
        if new_project_name:
            current_time = datetime.datetime.now().strftime("%H:%M %d.%m.%y")
            self.projects.append({
                "name": new_project_name,
                "time_spent": 0,
                "created_at": current_time,
                "last_tracked": "Never"
            })
            self.save_projects()

    def edit_project(self, project):
        """Open a dialog to edit all details of the project."""
        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Edit Project: {project['name']}")

        # Project Name
        tk.Label(edit_window, text="Project Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        name_entry = tk.Entry(edit_window, width=30)
        name_entry.insert(0, project["name"])
        name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Time Spent
        tk.Label(edit_window, text="Time Spent (seconds):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        time_entry = tk.Entry(edit_window, width=30)
        time_entry.insert(0, str(project["time_spent"]))
        time_entry.grid(row=1, column=1, padx=10, pady=5)

        # Created At
        tk.Label(edit_window, text="Created At:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        created_entry = tk.Entry(edit_window, width=30)
        created_entry.insert(0, project["created_at"])
        created_entry.grid(row=2, column=1, padx=10, pady=5)

        # Last Tracked
        tk.Label(edit_window, text="Last Tracked:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        last_tracked_entry = tk.Entry(edit_window, width=30)
        last_tracked_entry.insert(0, project["last_tracked"])
        last_tracked_entry.grid(row=3, column=1, padx=10, pady=5)

        # Save Button
        def save_changes():
            project["name"] = name_entry.get()
            try:
                project["time_spent"] = int(time_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Time Spent must be an integer.")
                return
            project["created_at"] = created_entry.get()
            project["last_tracked"] = last_tracked_entry.get()
            self.save_projects()
            edit_window.destroy()

        save_button = tk.Button(edit_window, text="Save", command=save_changes)
        save_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Cancel Button
        cancel_button = tk.Button(edit_window, text="Cancel", command=edit_window.destroy)
        cancel_button.grid(row=5, column=0, columnspan=2, pady=5)

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
            project["last_tracked"] = datetime.datetime.now().strftime("%H:%M %d.%m.%y")
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

    def show_project_details(self, project):
        """Open a new window to display project details."""
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Details for {project['name']}")

        # Display project name
        name_label = tk.Label(details_window, text=f"Project Name: {project['name']}", font=("Arial", 14))
        name_label.pack(pady=10)

        # Display time spent
        time_label = tk.Label(details_window, text=f"Time Spent: {self.format_time(project['time_spent'])}", font=("Arial", 14))
        time_label.pack(pady=10)

        # Display creation date
        created_label = tk.Label(details_window, text=f"Created At: {project['created_at']}", font=("Arial", 14))
        created_label.pack(pady=10)

        # Display last tracked time
        last_tracked_label = tk.Label(details_window, text=f"Last Tracked: {project['last_tracked']}", font=("Arial", 14))
        last_tracked_label.pack(pady=10)

        # Close button
        close_button = tk.Button(details_window, text="Close", command=details_window.destroy)
        close_button.pack(pady=10)

    def load_custom_file(self):
        from tkinter import filedialog

        # Open a file dialog to select a JSON file
        file_path = filedialog.askopenfilename(
            title="Select a JSON File",
            filetypes=(("JSON Files", "*.json"), ("All Files", "*.*"))
        )

        if file_path:
            # Save the path to the configuration file
            config_path = os.path.join(os.path.dirname(__file__), "config.json")
            with open(config_path, "w") as config_file:
                json.dump({"last_loaded_file": file_path}, config_file)

            # Reload projects from the new file
            self.projects = self.load_projects()
            self.refresh_project_list()
            messagebox.showinfo("Success", f"Loaded projects from: {file_path}")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingProjectTrackerApp(root)
    root.mainloop()