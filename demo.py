import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def run_demo():
    print("--- Starting Demo ---")

    # 1. Create a user with a balance
    user_id = "user_123"
    initial_balance = 1000
    # In a real app, you'd have an endpoint for this. We'll just set it in the store.
    from app.payment import store
    store.set_user_balance(user_id, initial_balance)
    print(f"Created user '{user_id}' with balance: {initial_balance}\n")

    # 2. Run a successful charge
    print("--- Running a successful charge ---")
    charge_amount = 100
    try:
        # Create and reserve
        response = requests.post(f"{BASE_URL}/charge", json={"user_id": user_id, "amount": charge_amount})
        response.raise_for_status()
        charge1 = response.json()
        charge1_id = charge1['id']
        print(f"Charge {charge1_id} created and funds reserved.")
        
        # Manually set the fail flag to False for this successful case
        from app.payment import service
        service.SHOULD_FAIL_CONFIRMATION = False

        # Confirm
        response = requests.post(f"{BASE_URL}/charge/{charge1_id}/confirm")
        response.raise_for_status()
        print(f"Charge {charge1_id} confirmed successfully.")
        print(f"Current balance for {user_id}: {store.get_user_balance(user_id)}\n")

    except requests.exceptions.RequestException as e:
        print(f"Error during successful charge: {e}")
        if e.response:
            print(f"Response: {e.response.text}")


    # 3. Run a charge that fails, triggers rollback, and then the bug
    print("--- Running charge that will fail, be rolled back, and retried ---")
    
    # Reset the flag to ensure the first confirmation fails
    from app.payment import service
    service.SHOULD_FAIL_CONFIRMATION = True
    
    charge_amount_2 = 250
    try:
        # Create and reserve
        response = requests.post(f"{BASE_URL}/charge", json={"user_id": user_id, "amount": charge_amount_2})
        response.raise_for_status()
        charge2 = response.json()
        charge2_id = charge2['id']
        print(f"Charge {charge2_id} created and funds reserved.")
        print(f"Balance after reservation for {user_id}: {store.get_user_balance(user_id)}")

        # Attempt to confirm (this will fail and trigger rollback)
        print("\nAttempting to confirm charge (expected to fail)...")
        try:
            requests.post(f"{BASE_URL}/charge/{charge2_id}/confirm")
        except requests.exceptions.HTTPError as e:
            print(f"As expected, confirmation failed: {e.response.status_code} {e.response.text}")
            print(f"Balance after automatic rollback for {user_id}: {store.get_user_balance(user_id)}")

        # Retry confirmation (this will succeed, but will have triggered the bug)
        print("\nRetrying confirmation...")
        
        # Here's the core of the incident: the client retries the confirmation.
        # The service's confirm_charge endpoint calls rollback_charge again on failure.
        # But our confirmation will succeed this time.
        # Let's simulate the retry from the client.
        
        # The bug is in the fact that `rollback_charge` is not idempotent.
        # Let's manually call rollback again to demonstrate.
        print("\n--- Triggering the Double-Credit Bug ---")
        print("An external system or a manual retry now erroneously calls rollback again...")
        
        # The client sees the failure, and instead of retrying `confirm`,
        # maybe it retries the whole operation or has a bug where it calls `rollback`.
        # To demonstrate the bug in `rollback_charge` directly:
        
        # Let's reset the state to RESERVED to simulate a retry of `confirm`
        # after a rollback.
        
        charge_to_break = store.get_charge(charge2_id)
        charge_to_break.state = "RESERVED"
        store.save_charge(charge_to_break)
        # We also need to debit the money again for the scenario to make sense
        store.set_user_balance(user_id, store.get_user_balance(user_id) - charge_amount_2)

        print(f"\nSimulating state before retry: Charge state is RESERVED, balance is {store.get_user_balance(user_id)}")
        
        # Now, let's retry the failing confirmation
        from app.payment import service
        service.SHOULD_FAIL_CONFIRMATION = True # Make it fail again
        
        print("\nRetrying the confirmation that fails and triggers the buggy rollback...")
        try:
            requests.post(f"{BASE_URL}/charge/{charge2_id}/confirm")
        except requests.exceptions.HTTPError as e:
            print(f"Confirmation failed again: {e.response.status_code}")
            print(f"Balance after SECOND rollback for {user_id}: {store.get_user_balance(user_id)}")
            print("\nBUG TRIGGERED: The balance is now higher than it should be due to double credit.")

    except requests.exceptions.RequestException as e:
        print(f"Error during failing charge scenario: {e}")
        if e.response:
            print(f"Response: {e.response.text}")
            
    print("\n--- Demo Finished ---")
    print(f"Final balance for {user_id}: {store.get_user_balance(user_id)}")
    expected_balance = initial_balance - charge_amount
    print(f"Expected balance for {user_id}: {expected_balance}")
    if store.get_user_balance(user_id) > expected_balance:
        print("Double-credit bug successfully reproduced!")

if __name__ == "__main__":
    # This script is intended to be run while the FastAPI app is running.
    # You would typically run `uvicorn app.main:app` first.
    # However, to make it self-contained for demonstration, we can simulate the calls.
    # This is not ideal, but works for this specific case.
    
    # A better approach is to run the app and this script separately.
    # The instructions will reflect that.
    print("This script sends requests to the running FastAPI application.")
    print("Please run 'uv run uvicorn app.main:app --reload' in another terminal first.")
    
    user_input = input("Is the server running? (y/n): ")
    if user_input.lower() == 'y':
        run_demo()
    else:
        print("Please start the server and run this script again.")