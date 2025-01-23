from enum import StrEnum

class ContentType(StrEnum):
    PDF = "application/pdf"
    TEXT_PLAIN = "text/plain"
    TEXT_CSV = "text/csv"
    IMAGE_PNG = "image/png"
    IMAGE_JPEG = "image/jpeg"
    IMAGE_JPG = "image/jpg"

    @classmethod
    def text_types(cls):
        return [cls.TEXT_PLAIN, cls.TEXT_CSV]

    @classmethod
    def image_types(cls):
        return [cls.IMAGE_PNG, cls.IMAGE_JPEG, cls.IMAGE_JPG]

POSSIBLE_VECTOR_DB_CONTENT_TYPE = (
    ContentType.TEXT_PLAIN,
    ContentType.PDF,
)


class ProcessState(StrEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"
    CANCEL = "cancel"


MAX_FILE_SIZE = 10 * 1024 * 1024
