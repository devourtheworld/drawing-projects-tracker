class ProjectList:
    def __init__(self, project_controller):
        self.project_controller = project_controller
        self.projects = []
    
    def refresh_list(self):
        self.projects = self.project_controller.load_projects()
        # Code to update the UI with the new list of projects goes here

    def on_project_selected(self, project_name):
        # Code to handle the selection of a project goes here
        pass

    def display_projects(self):
        # Code to display the list of projects in the UI goes here
        pass