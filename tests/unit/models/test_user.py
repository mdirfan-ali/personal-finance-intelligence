import pytest

from finance import Currency, User


@pytest.fixture
def valid_user():
    return User.create("Md Irfan Ali", "USD", 5000.00)


class TestUserCreation:
    
    def test_valid_user(self, valid_user):
        assert valid_user.name == "Md Irfan Ali"
        assert valid_user.currency == Currency.USD
        assert valid_user.income == 5000.00
    
    def test_name_strips_whitespace(self):
        user = User.create("  Md Irfan Ali  ", "EUR", 3000)
        
        assert user.name == "Md Irfan Ali"
    
    def test_currency_case_insensitive(self):
        user1 = User.create("A", "usd", 1000)
        user2 = User.create("B", "USD", 1000)
        
        assert user1.currency == user2.currency
    
    def test_income_integer_converts_to_float(self):
        user = User.create("Test", "GBP", 5000)
        
        assert isinstance(user.income, float)
        assert user.income == 5000.0


class TestUserUpdate:
    
    def test_user_update(self, valid_user):
        updated_user = valid_user.update(currency_code = "INR", income = 7700)

        assert updated_user.currency == Currency.INR
        assert updated_user.income == 7700
    

class TestUserValidation:
    
    def test_empty_name_raises_valueerror(self):
        with pytest.raises(ValueError, match="Name cannot be empty"):
            User.create("", "USD", 5000)
    
    def test_whitespace_name_raises_valueerror(self):
        with pytest.raises(ValueError, match="Name cannot be empty"):
            User.create("   ", "USD", 5000)
    
    def test_negative_income_raises_valueerror(self):
        with pytest.raises(ValueError, match="positive"):
            User.create("John", "USD", -100)
    
    def test_zero_income_raises_valueerror(self):
        with pytest.raises(ValueError, match="positive"):
            User.create("John", "USD", 0)
    
    def test_invalid_currency_raises_valueerror(self):
        with pytest.raises(ValueError, match="Invalid currency"):
            User.create("John", "XYZ", 5000)
    
    def test_unrealistic_income_raises_valueerror(self):
        with pytest.raises(ValueError, match="unrealistic"):
            User.create("John", "USD", 100_000_000)


class TestUserBehavior:
    
    def test_display_income_formatting(self, valid_user):
        result = valid_user.display_income()
        
        assert result == "USD 5,000.00"
    
    def test_immutable_cannot_modify(self, valid_user):
        with pytest.raises(Exception):
            valid_user.name = "Jane"
    
    def test_immutable_cannot_add_attribute(self, valid_user):
        with pytest.raises(Exception):
            valid_user.age = 25


class TestCurrencyEnum:
    
    def test_currency_values(self):
        assert Currency.USD.value == "USD"
        assert Currency.BDT.value == "BDT"
    
    def test_currency_from_string(self):
        curr = Currency("EUR")
        
        assert curr == Currency.EUR