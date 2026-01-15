from . import store
from .models import Charge, ChargeState
import logging

logging.basicConfig(level=logging.INFO)


SHOULD_FAIL_CONFIRMATION = True

def create_charge(user_id: str, amount: int) -> Charge:
    """
    Creates a charge and reserves funds from the user's balance.
    """
    logging.info(f"Creating charge for user {user_id} with amount {amount}")
    charge = Charge(user_id=user_id, amount=amount)
    store.save_charge(charge)
    reserve_funds(charge.id)
    return charge

def reserve_funds(charge_id: str):
    """
    Reserves funds for a specific charge.
    """
    charge = store.get_charge(charge_id)
    if not charge:
        raise ValueError("Charge not found")

    user_id = charge.user_id
    amount = charge.amount
    balance = store.get_user_balance(user_id)

    if balance < amount:
        raise ValueError("Insufficient funds")

    # Deduct balance
    store.set_user_balance(user_id, balance - amount)
    charge.state = ChargeState.RESERVED
    store.save_charge(charge)
    logging.info(f"Reserved {amount} for charge {charge_id}. New balance for user {user_id}: {store.get_user_balance(user_id)}")

def confirm_charge(charge_id: str):
    """
    Confirms a charge. This is where a transient error is simulated.
    """
    global SHOULD_FAIL_CONFIRMATION
    charge = store.get_charge(charge_id)
    if not charge:
        raise ValueError("Charge not found")

    if charge.state != ChargeState.RESERVED:
        raise ValueError("Charge not in RESERVED state")

    # Simulate a transient failure on the first attempt
    if SHOULD_FAIL_CONFIRMATION:
        SHOULD_FAIL_CONFIRMATION = False
        logging.error(f"Simulating transient failure for charge {charge_id}")
        raise IOError("Failed to connect to payment processor")

    charge.state = ChargeState.CONFIRMED
    store.save_charge(charge)
    logging.info(f"Confirmed charge {charge_id}")

def rollback_charge(charge_id: str):
    """
    Rolls back a charge by restoring the user's balance.
    This function is idempotent - multiple calls return the same result
    without crediting funds more than once.
    """
    charge = store.get_charge(charge_id)
    if not charge:
        raise ValueError("Charge not found")

    # Idempotency check: if already rolled back, return existing charge
    if charge.state == ChargeState.ROLLED_BACK:
        logging.info(f"Charge {charge_id} already rolled back. Returning existing state (idempotent).")
        return charge

    # Only allow rollback from RESERVED state
    if charge.state != ChargeState.RESERVED:
        raise ValueError(f"Cannot rollback charge in {charge.state.value} state. Only RESERVED charges can be rolled back.")

    user_id = charge.user_id
    amount = charge.amount
    balance = store.get_user_balance(user_id)

    store.set_user_balance(user_id, balance + amount)

    charge.state = ChargeState.ROLLED_BACK
    store.save_charge(charge)
    logging.warning(f"Rolled back charge {charge_id}. Restored {amount} to user {user_id}. New balance: {store.get_user_balance(user_id)}")
    return charge


def refund_charge(charge_id: str):
    """
    Refunds a confirmed charge.
    """
    charge = store.get_charge(charge_id)
    if not charge:
        raise ValueError("Charge not found")

    if charge.state != ChargeState.CONFIRMED:
        raise ValueError("Cannot refund a charge that is not confirmed.")

    user_id = charge.user_id
    amount = charge.amount
    balance = store.get_user_balance(user_id)


    store.set_user_balance(user_id, balance + amount)

    charge.state = ChargeState.REFUNDED
    store.save_charge(charge)
    logging.info(f"Refunded {amount} for charge {charge_id}. New balance for {user_id}: {store.get_user_balance(user_id)}")
