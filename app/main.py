from fastapi import FastAPI

from app.routers import auth, categories, expenses

app = FastAPI(title="Expense Tracker API")

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(expenses.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}