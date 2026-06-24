from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Self


class Currency(Enum):
    
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    BDT = "BDT"
    AED = "AED"
    INR = "INR"


@dataclass(frozen=True, slots=True)

class User:

    name: str
    currency: Currency
    income: float
    
    def __post_init__(self) -> None:

        self._validate_name()
        self._validate_income()


    def _validate_name(self) -> None:

        cleaned = self.name.strip()

        if not cleaned:
            raise ValueError("Name cannot be empty")
        
        if len(cleaned) > 100:
            raise ValueError(f"Name too long:{len(cleaned)} chars (max 100)")
    

    def _validate_income(self) -> None:

        if self.income <= 0:
            raise ValueError(
                f"Income must be positive, got {self.income}"
            )

        if self.income > 10_000_000:
            raise ValueError(f"Income seems unrealistic: {self.income}")


    def display_income(self) -> str:

        return f"{self.currency.value} {self.income:,.2f}"

    @classmethod
    def create(
        cls,
        name: str,
        currency_code:str,
        income:float
    ) -> Self:

        try:
            currency = Currency(currency_code.upper())
        except ValueError:
            allowed = [c.value for c in Currency]
            raise ValueError(
                f"Invalid currency '{currency_code}'."
                f"Allowed: {','.join(allowed)}"
            ) from None
        
        return cls(
            name=name.strip(),
            currency=currency,
            income=float(income)
        )
