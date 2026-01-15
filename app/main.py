from fastapi import FastAPI
from app.api import routes

app = FastAPI(title="Incident Memory Demo")

app.include_router(routes.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Incident Memory Demo API"}
