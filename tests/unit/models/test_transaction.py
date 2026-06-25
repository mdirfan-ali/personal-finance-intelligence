import pytest
from datetime import date
from finance.models.transaction import Transaction,TransactionType

@pytest.fixture
def expense_tx():
    return Transaction.create(500, "expense", "Food", "Lunch")

@pytest.fixture
def income_tx():
    return Transaction.create(50000, "income", "Salary")

class TestTransactionCreation:
    
    def test_valid_expense(self,expense_tx):
        assert expense_tx.amount == 500.0
        assert expense_tx.type == TransactionType.EXPENSE 
        assert expense_tx.category == "Food" 
        assert expense_tx.description == "Lunch"

    def test_valid_income(self,income_tx):
        assert income_tx.amount == 50000.0
        assert income_tx.type == TransactionType.INCOME
        assert income_tx.category == "Salary"
    
    def test_each_transaction_gets_unique_id(self):
        tx1 = Transaction.create(100,"expense","Food")
        tx2 = Transaction.create(100,"expense","Food")

        assert tx1.id != tx2.id

class TestTransactionValidation:

    def test_zero_amount_raises(self):
        with pytest.raises(ValueError, match = "must be positive"):
            Transaction.create(0,"expense","Food")
    
    def test_negative_amount_raises(self):
        with pytest.raises(ValueError, match="must be positive"):
            Transaction.create(-50, "expense", "Food")

class TestTransactionProperties:

    def test_is_income_true_for_income(self,income_tx):
        assert income_tx.is_income is True
        assert income_tx.is_expense is False

class TestTransactionUpdate:

    def test_update_returns_new_object_and_update_amount(self,expense_tx):
        updated = expense_tx.update(amount=800)
        assert updated is not expense_tx
        assert expense_tx.amount == 500.0
        assert updated.amount == 800.0