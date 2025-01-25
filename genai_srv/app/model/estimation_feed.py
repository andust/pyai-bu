from pydantic import BaseModel

from app.constants.common import ComplexityLevel


class EstimationFeed(BaseModel):
    id: str | None = None
    title: str
    description: str
    complexity: ComplexityLevel
    developer_id: str
    estimated_time_hours: int
    actual_time_hours: int
    tech_stack: list[str]

    @staticmethod
    def from_dict(data: dict):
        return EstimationFeed(
            id=str(data.get("_id", "")) or None,
            title=data.get("title", ""),
            description=data.get("description", ""),
            complexity=data.get("complexity", ComplexityLevel.CRITICAL),
            developer_id=data.get("developer_id", ""),
            estimated_time_hours=data.get("estimated_time_hours", 0),
            actual_time_hours=data.get("actual_time_hours", 0),
            tech_stack=data.get("tech_stack", []),
        )
