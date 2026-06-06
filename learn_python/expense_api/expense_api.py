from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from typing import Optional
from datetime import date
from pydantic import BaseModel
import uuid

import expense
import json

TASK_FILE = "expenses.json"
app = FastAPI()

class ExpenseRequest(BaseModel):
    title: str
    amount: float
    category: str
    date: date
    notes: Optional[str] = None


@app.get("/expenses")
def get_tasks():
    return expense.list_expenses()

@app.post("/expense")
def add_expense(expense_req: ExpenseRequest):
    new_expense = expense.Expense(
        id=str(uuid.uuid4()),
        title=expense_req.title,
        amount=expense_req.amount,
        category=expense_req.category,
        date=expense_req.date,
        notes=expense_req.notes
    )
    expense.add_expense(new_expense)
    return new_expense

@app.delete("/expenses/{expense_id}")
def delete_task(expense_id: str):
    expense.remove_expense(expense_id)

@app.get("/expenses/categorize")
def get_tasks_category():
    return expense.categorize_expenses()
