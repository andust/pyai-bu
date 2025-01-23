from bson import ObjectId

from app.constants.common import ComplexityLevel


PROJECTS = [
    {
        "_id": ObjectId("778e149ba74ac80c6182cfe1"),
        "title": "Project One",
        "description": "description 1",
        "complexity": ComplexityLevel.HIGH,
    },
    {
        "_id": ObjectId("778e149ba74ac80c6182cfe2"),
        "title": "Project Two",
        "description": "description 2",
        "complexity": ComplexityLevel.LOW,
    },
    {
        "_id": ObjectId("778e149ba74ac80c6182cfe3"),
        "title": "Project Three",
        "description": "description 3",
        "complexity": ComplexityLevel.MEDIUM,
    },
]
