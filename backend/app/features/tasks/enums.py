from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    OVERDUE = "OVERDUE"

class TaskPriority(str, Enum):
    OPTIONAL = "OPTIONAL"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    IMPORTANT = "IMPORTANT"