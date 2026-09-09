from enum import Enum

class NotificationStatus(str, Enum):
    FAILED = "FAILED"
    PENDING = "PENDING"
    DELIVERED = "DELIVERED"
    SEEN = "SEEN"