from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Category, Expense, User
from app.schemas import ExpenseCreate, ExpenseResponse, ExpenseUpdate
from app.security import get_current_user

router = APIRouter(prefix="/expenses", tags=["Expenses"])


def _get_user_category(db: Session, category_id: int, user_id: int) -> Category:
    category = db.scalar(
        select(Category).where(Category.id == category_id, Category.user_id == user_id)
    )
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category


@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(
    data: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _get_user_category(db, data.category_id, current_user.id)

    expense_data = data.model_dump(exclude_none=True)
    expense = Expense(**expense_data, user_id=current_user.id)
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


@router.get("/", response_model=list[ExpenseResponse])
def get_expenses(
    category_id: int | None = Query(default=None),
    date_from: datetime | None = Query(default=None),
    date_to: datetime | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stmt = select(Expense).where(Expense.user_id == current_user.id)

    if category_id is not None:
        stmt = stmt.where(Expense.category_id == category_id)
    if date_from is not None:
        stmt = stmt.where(Expense.spent_at >= date_from)
    if date_to is not None:
        stmt = stmt.where(Expense.spent_at <= date_to)

    stmt = stmt.order_by(Expense.spent_at.desc())
    return db.scalars(stmt).all()


@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    expense = db.scalar(
        select(Expense).where(Expense.id == expense_id, Expense.user_id == current_user.id)
    )
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    return expense


@router.patch("/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    data: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    expense = db.scalar(
        select(Expense).where(Expense.id == expense_id, Expense.user_id == current_user.id)
    )
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")

    update_data = data.model_dump(exclude_unset=True)
    if "category_id" in update_data:
        _get_user_category(db, update_data["category_id"], current_user.id)

    for field, value in update_data.items():
        setattr(expense, field, value)

    db.commit()
    db.refresh(expense)
    return expense


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    expense = db.scalar(
        select(Expense).where(Expense.id == expense_id, Expense.user_id == current_user.id)
    )
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")

    db.delete(expense)
    db.commit()