## Relations
@bug_fixes/double_credit_bug_analysis.md
@structure/entry_points.md

## Raw Concept
**Task:**
Document the demo script execution workflow

**Changes:**
- Detailed the demo script workflow and verification steps

**Files:**
- demo.py

**Flow:**
setup -> success case -> fail/auto-rollback case -> manual/retry rollback -> verify bug

**Timestamp:** 2026-01-15

## Narrative
### Structure
- `demo.py`: Main script for bug reproduction.
- `run_demo()`: Orchestrates the multi-step scenario.

### Dependencies
- requests
- app/payment/store.py
- app/payment/service.py
- FastAPI server (running on http://127.0.0.1:8000)

### Features
### Demo Execution Workflow
The `demo.py` script executes the following steps to reproduce the double-credit bug:

1. **Setup**: Initializes `user_123` with a balance of 1000.
2. **Step 1: Successful Charge**: 
   - Creates a 100-unit charge.
   - Confirms it successfully.
   - Result: Balance remains 900 (1000 - 100).
3. **Step 2: Failing Charge with Rollback**:
   - Sets `SHOULD_FAIL_CONFIRMATION = True`.
   - Creates a 250-unit charge.
   - Attempted confirmation fails; API automatically calls `rollback_charge`.
   - Result: Balance is restored to 900.
4. **Step 3: Trigger Double-Credit Bug**:
   - Simulates a retry or external system error by manually calling `rollback_charge` again on the same charge ID.
   - Result: Balance becomes 1150 (900 + 250).
5. **Step 4: Verification**:
   - Compares final balance against the expected balance (Initial - Successful charges).
   - If `final > expected`, the double-credit bug is confirmed.

### Key Internal Interactions
- Uses `requests` to call API endpoints: `POST /charge`, `POST /charge/{id}/confirm`, `POST /charge/{id}/rollback`.
- Directly imports `store` and `service` for setup and state manipulation during the demo.
