from enum import Enum
from app.features.users.enums import UserRoles

class LabelOwner(str, Enum):
    SYSTEM = "SYSTEM"
    ADMIN = UserRoles.ADMIN.value
    USER = UserRoles.USER.value