from enum import Enum

class LabelOwner(str, Enum):
    SYSTEM = "SYSTEM"
    ADMIN = "ADMIN"
    USER = "USER"