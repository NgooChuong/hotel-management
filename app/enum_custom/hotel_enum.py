import enum


class ReservationStateEnum(enum.Enum):
    DRAFT = "draft"
    CONFIRM = "confirm"
    DONE = "done"
    CANCEL = "cancel"


class RoomStateEnum(enum.Enum):
    AVAILABLE = "available"
    BOOKED = "booked"
    MAINTENANCE = "maintenance"
