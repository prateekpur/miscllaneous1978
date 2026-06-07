from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from typing import Optional
from datetime import date
from pydantic import BaseModel
import uuid
import expense
from dataclasses import asdict
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
def get_expenses():
    jsonarr = [asdict(e) for e in expense.list_expenses()]
    return {"success": True,
            "message": "List of all expenses",
            "data": jsonarr}

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
    return {"success": True,
            "message": "Expense created successfully",
            "data": asdict(new_expense)}

@app.delete("/expenses/{expense_id}", status_code=200)
def delete_task(expense_id: str):
    del_exp = expense.remove_expense(expense_id)
    if (del_exp is not None) :
        return {"success": True,
                "message": "Expense deleted successfully",
                "data": del_exp}
    raise HTTPException(status_code=404, detail="Expense not found")

@app.get("/expenses/categorize")
def get_tasks_category():
    return {"success": True,
            "message": "Category summary generated",
            "data": expense.categorize_expenses()}

@app.post("/saveExpense")
def save_expense():
    try:
        expense.save_expenses(TASK_FILE)
        return {"message": "Expenses saved successfully"}
    except OSError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save expenses: {e}"
        ) from e

@app.post("/loadExpense")
def load_expense():
    try:
        expense.read_expenses(TASK_FILE)
        return {"message": "Expenses loaded successfully"}
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense file not found"
        ) from e
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Expense file contains invalid JSON"
        ) from e
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid expense data: {e}"
        ) from e
    except OSError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load expenses: {e}"
        ) from e