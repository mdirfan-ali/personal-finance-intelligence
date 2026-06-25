from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import date
from enum import Enum
from typing import Self
from uuid import uuid4

class TransactionType(Enum):
    INCOME = "income"
    EXPENSE = "expense"

@dataclass(frozen=True, slots=True)
class Transaction:
    amount: float
    type: TransactionType
    category: str
    description: str
    date: date
    id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        self._validate_amount()
        self._validate_category()
    
    def _validate_amount(self) -> None:
        if self.amount <= 0:
            raise ValueError(f"Amount must be positive, got {self.amount}")
    
    def _validate_category(self) -> None:
        if not self.category.strip():
            raise ValueError("Category cannot be empty")

    @property
    def is_income(self) -> bool:
        return self.type is TransactionType.INCOME
    
    @property
    def is_expense(self) -> bool:
        return self.type is TransactionType.EXPENSE

    @property
    def signed_amount(self) -> float:
        return self.amount if self.is_income else -self.amount

    @classmethod
    def create(
        cls,
        amount: float,
        type_code: str,
        category: str,
        description: str = "",
        on: date | None = None
    ) -> Self:

        try:
            tx_type = TransactionType(type_code.lower())
        except ValueError:
            allowed = [t.value for t in TransactionType]
            raise ValueError(
                f"Invalid type '{type_code}'. Allowed: {', '.join(allowed)}"
            ) from None
        
        return cls(
            amount = float(amount),
            type = tx_type,
            category = category.strip(),
            description = description.strip(),
            date = on or date.today()
        )

    def update(
        self,
        *,
        amount: float | None = None,
        category: str | None = None,
        description: str | None = None,
        on: date | None = None
    ) -> Self:

        changes:dict = {}
        
        if amount is not None:
            changes["amount"] = float(amount)
        
        if category is not None:
            changes["category"] = category.strip()

        if description is not None:
            changes["description"] = description.strip()
        
        if on is not None:
            changes["date"] = on

        return replace(self, **changes) 