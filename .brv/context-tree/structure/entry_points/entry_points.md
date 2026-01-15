## Relations
@structure/project_overview.md
@testing/bug_reproduction_demo.md

## Raw Concept
**Task:**
Document the project entry points and startup flow

**Changes:**
- Added entry points and startup flow documentation

**Files:**
- app/main.py
- demo.py

**Flow:**
1. FastAPI app created in main.py -> 2. Routes registered -> 3. Uvicorn serves app (port 8000) -> 4. Demo script sends requests

**Timestamp:** 2026-01-15

## Narrative
### Structure
- `app/main.py`: Entry point for the FastAPI web server.
- `demo.py`: Entry point for the bug reproduction script.

### Dependencies
- app/main.py
- demo.py
- uvicorn
- python

### Features
- Web Server Entry Point: `uvicorn app.main:app --reload`
- Demo Script Entry Point: `python demo.py`
- Startup Flow: FastAPI app creation -> Route registration -> Uvicorn hosting -> Demo script execution
