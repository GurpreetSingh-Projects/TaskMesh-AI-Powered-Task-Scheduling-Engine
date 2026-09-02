from enum import Enum

class LabelOwner(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    SYSTEM = "SYSTEM"