## Relations
@business_logic/payment_processing_logic.md
@api_design/payment_api.md

## Raw Concept
**Task:**
Document payment data models and state transitions

**Changes:**
- Added detailed data model and state transition documentation

**Files:**
- app/payment/models.py
- app/api/routes.py

**Flow:**
Pydantic models define the structure of data as it moves through the state machine.

**Timestamp:** 2026-01-15

## Narrative
### Structure
- `app/payment/models.py`: Primary location for data models.
- `app/api/routes.py`: Defines `CreateChargeRequest`.

### Dependencies
- pydantic
- enum
- uuid

### Features
### ChargeState Enum
Defines the lifecycle of a charge:
- `CREATED`: Initial state.
- `RESERVED`: Funds deducted from user balance.
- `CONFIRMED`: Transaction finalized.
- `ROLLED_BACK`: Funds returned to user (non-idempotent in this system).
- `REFUNDED`: Funds returned after successful confirmation.

### Charge Model
Pydantic model representing a payment transaction:
- `id`: Unique identifier (UUID).
- `user_id`: Target user.
- `amount`: Integer value of the charge.
- `state`: Current `ChargeState`.

### State Transitions (Logic-driven)
- **Reservation**: `CREATED` → `RESERVED`
- **Confirmation**: `RESERVED` → `CONFIRMED`
- **Rollback**: `RESERVED` → `ROLLED_BACK`
- **Refund**: `CONFIRMED` → `REFUNDED`
