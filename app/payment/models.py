from enum import Enum
from pydantic import BaseModel
import uuid

class ChargeState(str, Enum):
    CREATED = "CREATED"
    RESERVED = "RESERVED"
    CONFIRMED = "CONFIRMED"
    ROLLED_BACK = "ROLLED_BACK"
    REFUNDED = "REFUNDED"

class Charge(BaseModel):
    id: str = str(uuid.uuid4())
    user_id: str
    amount: int
    state: ChargeState = ChargeState.CREATED
