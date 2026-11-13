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

RankPriority = {
    TaskPriority.OPTIONAL.value: 0,
    TaskPriority.NORMAL.value: 1,
    TaskPriority.HIGH.value: 2,
    TaskPriority.IMPORTANT.value: 3,
}

if set(RankPriority) != {p.value for p in TaskPriority}:
    raise RuntimeError("PRIORITY_RANK is out of sync with TaskPriority")