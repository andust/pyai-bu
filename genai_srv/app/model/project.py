from pydantic import BaseModel

from app.constants.common import ComplexityLevel
from app.model.estimation import Estimation


class Project(BaseModel):
    id: str | None = None
    title: str
    description: str
    complexity: ComplexityLevel
    estimation: Estimation | None = None

    @staticmethod
    def from_dict(data: dict):
        estimation_data = data.get("estimation")
        return Project(
            id=str(data.get("_id")) or None,
            title=data.get("title", ""),
            description=data.get("description", ""),
            complexity=data.get("complexity", ComplexityLevel.CRITICAL),
            estimation=Estimation.from_dict(estimation_data)
            if estimation_data
            else None,
        )
