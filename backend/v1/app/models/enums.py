from enum import Enum

class TaskStatus(str, Enum):
    pending= "pending"
    in_progress= "in_progress"
    completed= "completed"

class TaskPriority(str, Enum):
    optional = "optional"
    normal = "normal"    
    high = "high"
    important = "important"
