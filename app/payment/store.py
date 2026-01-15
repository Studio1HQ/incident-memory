from typing import Dict
from .models import Charge


user_balances: Dict[str, int] = {}
charges: Dict[str, Charge] = {}

def get_user_balance(user_id: str) -> int:
    return user_balances.get(user_id, 0)

def set_user_balance(user_id: str, balance: int):
    user_balances[user_id] = balance

def get_charge(charge_id: str) -> Charge | None:
    return charges.get(charge_id)

def save_charge(charge: Charge):
    charges[charge.id] = charge
