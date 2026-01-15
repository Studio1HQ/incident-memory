## Relations
@api_design/payment_api.md
@bug_fixes/double_credit_bug_analysis.md

## Raw Concept
**Task:**
Document charge state machine and internal service flows

**Changes:**
- Updated business logic documentation with state machine and internal flows

**Files:**
- app/payment/service.py
- app/payment/models.py

**Flow:**
detailed state transitions and internal function calls

**Timestamp:** 2026-01-15

## Narrative
### Structure
- Logic implemented in `app/payment/service.py`
- State tracked via `ChargeState` enum in `app/payment/models.py`
- In-memory persistence via `app/payment/store.py`

### Dependencies
- app/payment/store.py
- app/payment/models.py

### Features
- **Charge State Machine**: `CREATED` → `RESERVED` → `CONFIRMED` → `REFUNDED` (or `RESERVED` → `ROLLED_BACK`).
- `create_charge` flow: Save charge -> `reserve_funds` (deduct balance, set `RESERVED`).
- `confirm_charge` flow: Check `RESERVED` state -> Simulate failure -> set `CONFIRMED`.
- `rollback_charge` flow: Restore balance -> set `ROLLED_BACK`. (NOT IDEMPOTENT)
- `refund_charge` flow: Check `CONFIRMED` state -> Restore balance -> set `REFUNDED`.
