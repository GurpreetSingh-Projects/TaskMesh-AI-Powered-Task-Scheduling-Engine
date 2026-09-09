from enum import Enum

class UserRoles(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"