# Drawing Project Tracker

This project is a drawing project tracker application built with Python. It allows users to manage their drawing projects by adding, editing, and deleting projects, as well as tracking the time spent on each project. The data is stored in a JSON file for easy access and modification.

## Features

- List of drawing projects with the ability to select and track time spent on each project.
- Add, edit, and delete projects through a user-friendly interface.
- Data is saved in a JSON file, ensuring persistence across sessions.

## Project Structure

```
drawing-project-tracker
├── src
│   ├── main.py                # Entry point of the application
│   ├── ui
│   │   ├── app_ui.py          # Main application window and UI integration
│   │   └── components
│   │       ├── project_list.py # Manages the display of the project list
│   │       └── project_editor.py# UI for adding, editing, and deleting projects
│   ├── models
│   │   └── project.py          # Defines the Project class
│   ├── controllers
│   │   └── project_controller.py# Manages interaction between UI and project data
│   └── data
│       └── projects.json       # Stores project data in JSON format
├── requirements.txt            # Lists project dependencies
├── README.md                   # Project documentation
└── .gitignore                  # Files to be ignored by version control
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/drawing-project-tracker.git
   ```
2. Navigate to the project directory:
   ```
   cd drawing-project-tracker
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```
   python src/main.py
   ```
2. Use the UI to manage your drawing projects. You can add new projects, edit existing ones, and track the time spent on each project.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.