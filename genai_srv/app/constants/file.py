from enum import Enum

POSSIBLE_VECTOR_DB_CONTENT_TYPE = (
    "text/plain",
    "application/pdf",
)


class ProcessState(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"
    CANCEL = "cancel"


MAX_FILE_SIZE = 10 * 1024 * 1024
