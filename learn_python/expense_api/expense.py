from dataclasses import dataclass
from fastapi import HTTPException
from datetime import date
from typing import Optional
import json
from dataclasses import asdict


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
        return []
    return expenses

def add_expense(exp):
    expenses.append(exp)
    #print(expenses)

def remove_expense(id):
    global expenses
    expense_obj = next((e for e in expenses if e.id == id), None)
    if not expense_obj:
        return None
    expenses.remove(expense_obj)
    return expense_obj

def categorize_expenses():
    categ_expenses = {}
    for exp in expenses :
        amt = exp.amount + categ_expenses.get(exp.category , 0.0)
        categ_expenses[exp.category] = amt
    return categ_expenses


def save_expenses(filename):
    #print(expenses)
    payload = []
    for e in expenses:
        item = asdict(e)
        # store date consistently as ISO string
        item["date"] = e.date.isoformat()
        payload.append(item)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(payload, f)

def read_expenses(filename):
    global expenses
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    parsed = []
    for item in data:
        try:
            raw_date = item.get("date")
            if not isinstance(raw_date, str):
                raise ValueError("date must be an ISO string")
            item["date"] = date.fromisoformat(raw_date)
            parsed.append(Expense(**item))
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid expense record: {e}") from e
    expenses = parsed
    return expenses