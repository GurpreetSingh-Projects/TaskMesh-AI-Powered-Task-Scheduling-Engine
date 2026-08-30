from enum import Enum

class LabelOwner(str, Enum):
    admin = "ADMIN"
    user = "USER"
    system = "SYSTEM"