## Relations
@business_logic/payment_processing_logic.md
@bug_fixes/double_credit_bug_analysis.md

## Raw Concept
**Task:**
Document detailed API execution paths

**Changes:**
- Updated API documentation with detailed execution paths and error handling

**Files:**
- app/api/routes.py

**Flow:**
Request -> Route -> Service -> Response/Error Rollback

**Timestamp:** 2026-01-15

## Narrative
### Structure
- Route definitions in `app/api/routes.py`
- Exception handling for `ValueError` (400) and `IOError` (500)
- Integration with `app.payment.service` functions

### Dependencies
- app/payment/service.py
- app/payment/models.py

### Features
- **POST `/charge`**: Creates a new charge and reserves funds. Success returns `RESERVED` state.
- **POST `/charge/{charge_id}/confirm`**: Confirms a reserved charge. Triggers automatic `rollback_charge` on transient `IOError`.
- **POST `/charge/{charge_id}/rollback`**: Manually credits amount back to user. BUG: Non-idempotent.
- **POST `/charge/{charge_id}/refund`**: Refunds a `CONFIRMED` charge, returning funds to user balance.
