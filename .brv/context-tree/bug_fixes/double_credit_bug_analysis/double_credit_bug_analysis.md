## Relations
@business_logic/payment_processing_logic.md
@testing/bug_reproduction_demo.md
@design/shared_state_and_assumptions.md

## Raw Concept
**Task:**
Document the fix for the double-credit bug

**Changes:**
- Documented the idempotency fix for the double-credit bug

**Files:**
- app/payment/service.py

**Flow:**
transient error -> automatic rollback -> manual/retry rollback (now idempotent/safe)

**Timestamp:** 2026-01-15

## Narrative
### Structure
- `app/payment/service.py`: Contains the fixed `rollback_charge` implementation (lines 63-91).
- `app/api/routes.py`: Continues to handle the `confirm` -> `rollback` flow safely.

### Dependencies
- app/payment/service.py
- app/payment/store.py
- app/payment/models.py

### Features
### Bug Summary
- **Location**: `app/payment/service.py`, `rollback_charge()` function.
- **Root Cause**: Lack of idempotency. Multiple calls to rollback would credit the user's balance multiple times.
- **Fix Implementation**: 
  - Added an **idempotency guard**: Check if `charge.state == ChargeState.ROLLED_BACK` and return early.
  - Added **state validation**: Only allow rollback if the charge is in the `RESERVED` state.
  - This ensures that funds are credited exactly once, regardless of how many times the rollback is triggered (e.g., by retries).
- **Verification**: The `demo.py` script can still be used to verify that subsequent calls to rollback now return early without modifying the balance.
