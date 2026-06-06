from dataclasses import dataclass
import sys
from fastapi import HTTPException
from datetime import date
from typing import Optional

@dataclass
class Expense:
    id: str
    title: str
    amount: float
    category: str
    date: date
    notes: Optional[str] = None

expenses = []

def list_expenses():
    if not expenses :
        print ("No Expenses")
    return expenses

def add_expense(exp):
    expenses.append(exp)
    #print(expenses)

def remove_expense(id):
    global expenses
    expense_obj = next((e for e in expenses if e.id == id), None)
    if not expense_obj:
        raise HTTPException(status_code=404, detail="Expense not found")
    expenses.remove(expense_obj)
    return {"message": "deleted"}

def categorize_expenses():
    categ_expenses = {}
    for exp in expenses :
        amt = exp.amount + categ_expenses.get(exp.category , 0.0)
        categ_expenses[exp.category] = amt
    return categ_expenses