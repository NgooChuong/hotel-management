import enum


class StatusEnum(enum.Enum):
    SUCCESS = (200, "Success")
    CREATED = (201, 'Created')
    DELETE = (204, 'No Content')
    NOT_FOUND = (404, "Data not found")
    INTERNAL_ERROR = (500, "Internal server error")
    DELETE_ERROR = (1004, "Delete error")
    UPDATE_ERROR = (1003, "Update error")
    CREATE_ERROR = (1002, "Create error")

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
