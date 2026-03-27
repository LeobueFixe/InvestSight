import pytest
from decimal import Decimal


class TestDecimal:
    def test_decimal_field_precision(self):
        from apps.wallet.models import Holding

        field = Holding._meta.get_field("quantity")
        assert field.max_digits == 20
        assert field.decimal_places == 8

    def test_decimal_arithmetic(self):
        a = Decimal("100.00")
        b = Decimal("50.00")
        assert a - b == Decimal("50.00")
        assert a + b == Decimal("150.00")
        assert a * b == Decimal("5000.00")
