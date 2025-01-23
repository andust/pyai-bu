class ProjectNotFoundError(Exception):
    def __init__(self, project_id: str):
        super().__init__(f"Project with id '{project_id}' not found.")
