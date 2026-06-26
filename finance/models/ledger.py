from __future__ import annotations
from datetime import date
from finance.models.transaction import Transaction

class TransactionNotFoundError(Exception):
    pass

class Ledger:

    def __init__(self) -> None:
        self._transactions: dict[str, Transaction] = {}

    def add(self, tx: Transaction) -> Transaction:
        self._transactions[tx.id] = tx
        return tx

    def get(self, tx_id:str) -> Transaction:
        try:
            return self._transactions[tx_id]
        except KeyError:
            raise TransactionNotFoundError(
                f"No transaction exist with id '{tx_id}'"
            ) from None
    
    def all(self) -> list[Transaction]:
        return sorted(
            self._transactions.values(),
            key = lambda t: t.date,
            reverse = True
        )
    
    def edit(self, tx_id:str, **changes) -> Transaction:
        old = self.get(tx_id)
        updated = old.update(**changes)
        self._transactions[tx_id] = updated
        return updated
    
    def delete(self, tx_id:str) -> None:
        if tx_id not in self._transactions:
            raise TransactionNotFoundError(
                f"No transaction exist with id '{tx_id}'"
            ) from None

        del self._transactions[tx_id]

    @property
    def count(self) -> int:
        return len(self._transactions)

    @property
    def balance(self) -> float:
        return sum(t.signed_amount for t in self._transactions.values())