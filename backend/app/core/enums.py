from enum import Enum

class ActivationStatus(str, Enum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"
    
class DeliveryStatus(str, Enum):
    FAILED = "FAILED"
    PENDING = "PENDING"
    DELIVERED = "DELIVERED"
    SEEN = "SEEN"