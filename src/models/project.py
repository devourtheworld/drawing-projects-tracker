class Project:
    def __init__(self, name, time_spent=0):
        self.name = name
        self.time_spent = time_spent

    def to_dict(self):
        return {
            "name": self.name,
            "time_spent": self.time_spent
        }

    @classmethod
    def from_dict(cls, data):
        return cls(name=data["name"], time_spent=data["time_spent"])