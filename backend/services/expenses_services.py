from sqlalchemy.orm import Session
from datetime import date
from ..models.expenses import Expense
from ..schemas.expense import Expense as ExpenseSchema


def create_expense(
    db: Session,
    *,
    user_id: int,
    vendor: str,
    amount: float,
    expense_date: date,
    category: str,
    raw_text: str,
) -> Expense:
    expense = Expense(
        user_id=user_id,
        vendor=vendor,
        amount=amount,
        expense_date=expense_date,
        category=category,
        raw_text=raw_text,
    )
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


def to_schema(expense: Expense) -> ExpenseSchema:
    return ExpenseSchema(
        id=expense.id,
        user_id=expense.user_id,
        vendor=expense.vendor,
        amount=float(expense.amount),
        expense_date=expense.expense_date,
        category=expense.category,
        raw_text=expense.raw_text,
    )


