class ProjectController:
    def __init__(self, project_model, data_file):
        self.project_model = project_model
        self.data_file = data_file
        self.projects = self.load_projects()

    def load_projects(self):
        try:
            with open(self.data_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def save_projects(self):
        with open(self.data_file, 'w') as file:
            json.dump(self.projects, file)

    def add_project(self, name):
        new_project = self.project_model(name=name, time_spent=0)
        self.projects.append(new_project.to_dict())
        self.save_projects()

    def delete_project(self, project_name):
        self.projects = [project for project in self.projects if project['name'] != project_name]
        self.save_projects()

    def edit_project(self, old_name, new_name):
        for project in self.projects:
            if project['name'] == old_name:
                project['name'] = new_name
                self.save_projects()
                break

    def track_time(self, project_name, time_spent):
        for project in self.projects:
            if project['name'] == project_name:
                project['time_spent'] += time_spent
                self.save_projects()
                break

    def get_projects(self):
        return self.projects