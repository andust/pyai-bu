from pydantic import BaseModel

from app.constants.common import ComplexityLevel


class Estimation(BaseModel):
    result: str
    complexity: ComplexityLevel
    estimated_time_hours: int
    actual_time_hours: int
    tech_stack: list[str]

    @staticmethod
    def from_dict(data: dict):
        return Estimation(
            result=data.get("result", ""),
            complexity=data.get("complexity", ComplexityLevel.CRITICAL),
            estimated_time_hours=data.get("estimated_time_hours", 0),
            actual_time_hours=data.get("actual_time_hours", 0),
            tech_stack=data.get("tech_stack", []),
        )
