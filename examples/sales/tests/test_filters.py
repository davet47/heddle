from src.filters import included_sales, sales_in_region, sales_over
from src.types import Sale


def test_included_sales():
    kept = Sale(region="QLD", amount=10.0, completed=True)
    sales = [
        kept,
        Sale(region="NSW", amount=5.0, completed=False),
        Sale(region="VIC", amount=None, completed=True),
    ]
    assert included_sales(sales) == [kept]


def test_included_sales_preserves_order():
    first = Sale(region="QLD", amount=1.0, completed=True)
    second = Sale(region="NSW", amount=2.0, completed=True)
    sales = [first, Sale(region="VIC", amount=None, completed=True), second]
    assert included_sales(sales) == [first, second]


def test_sales_in_region():
    qld = Sale(region="QLD", amount=10.0, completed=True)
    sales = [
        qld,
        Sale(region="NSW", amount=5.0, completed=True),
        Sale(region="QLD", amount=None, completed=True),
    ]
    assert sales_in_region(sales, "QLD") == [qld]


def test_sales_over():
    big = Sale(region="QLD", amount=100.0, completed=True)
    sales = [
        big,
        Sale(region="QLD", amount=50.0, completed=True),
        Sale(region="NSW", amount=200.0, completed=False),
    ]
    assert sales_over(sales, 50.0) == [big]
