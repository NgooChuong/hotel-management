import enum


class StatusEnum(enum.Enum):
    SUCCESS = (200, "Success")
    CREATED = (201, 'Created')
    NOT_FOUND = (404, "Data not found")
    INTERNAL_ERROR = (500, "Internal server error")

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
