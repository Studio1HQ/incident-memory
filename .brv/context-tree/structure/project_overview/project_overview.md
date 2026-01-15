## Relations
@bug_fixes/double_credit_bug.md
@api_design/payment_endpoints.md

## Raw Concept
**Task:**
Document the incident-memory project structure and purpose

**Changes:**
- Initial curation of project structure and purpose

**Files:**
- app/main.py
- app/api/routes.py
- app/payment/service.py
- app/payment/store.py
- app/payment/models.py
- demo.py
- requirements.txt

**Flow:**
FastAPI -> routes -> service -> store

**Timestamp:** 2026-01-15

## Narrative
### Structure
- `app/main.py`: FastAPI app initialization
- `app/api/routes.py`: REST API endpoints
- `app/payment/service.py`: Business logic with bug
- `app/payment/store.py`: In-memory data store
- `app/payment/models.py`: Pydantic models
- `demo.py`: Bug reproduction script

### Dependencies
- FastAPI (web framework)
- Uvicorn (ASGI server)
- Pydantic (data validation)
- In-memory storage (dictionaries)

### Features
- Payment processing demo
- Intentional double-credit bug
- Transient failure simulation
- Non-idempotent rollback operations
