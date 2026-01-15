## Relations
@structure/project_overview.md
@business_logic/payment_processing_logic.md

## Raw Concept
**Task:**
Document shared state and system assumptions

**Changes:**
- Added documentation for shared state and system assumptions

**Files:**
- app/payment/store.py
- app/payment/models.py
- app/payment/service.py

**Flow:**
In-memory dictionaries serve as the source of truth for balances and charges.

**Timestamp:** 2026-01-15

## Narrative
### Structure
- `app/payment/store.py`: Implementation of the in-memory data store.
- `app/payment/models.py`: Definition of `Charge` and `ChargeState`.

### Dependencies
- app/payment/store.py
- app/payment/models.py

### Features
### Shared State (In-Memory)
- `user_balances`: Dictionary mapping `user_id` to `int` balance.
- `charges`: Dictionary mapping `charge_id` to `Charge` objects.

### System Assumptions
- **Single-process**: No distributed state management.
- **Ephemeral**: All data is lost on server restart (no persistence).
- **Concurrency**: No protection against race conditions.
- **Data Types**: All financial amounts are handled as integers.

### Business & Bug Assumptions
- User balances default to 0.
- Charges transition only from `RESERVED` to `CONFIRMED`.
- Rollbacks are assumed to be safe but are non-idempotent in this demo.
- `SHOULD_FAIL_CONFIRMATION` global flag is used to trigger simulation.
