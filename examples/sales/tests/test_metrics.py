from src.metrics import (
    average_sale,
    revenue_by_customer,
    revenue_by_region,
    revenue_share_by_region,
    sale_count_by_region,
    top_customers,
    total_revenue,
)
from src.types import Sale

SALES = [
    Sale(region="QLD", amount=100.0, completed=True, customer_id="c1"),
    Sale(region="QLD", amount=50.0, completed=True, customer_id="c2"),
    Sale(region="NSW", amount=50.0, completed=True, customer_id="c1"),
    Sale(region="VIC", amount=None, completed=True, customer_id="c3"),
    Sale(region="VIC", amount=25.0, completed=False, customer_id="c3"),
]


def test_total_revenue():
    assert total_revenue(SALES) == 200.0


def test_revenue_by_region():
    assert revenue_by_region(SALES) == {"QLD": 150.0, "NSW": 50.0}


def test_average_sale():
    sales = [
        Sale(region="QLD", amount=10.0, completed=True),
        Sale(region="NSW", amount=20.0, completed=True),
        Sale(region="VIC", amount=None, completed=True),
    ]
    assert average_sale(sales) == 15.0


def test_average_sale_empty():
    assert average_sale([]) == 0.0


def test_sale_count_by_region():
    assert sale_count_by_region(SALES) == {"QLD": 2, "NSW": 1}


def test_revenue_by_customer():
    assert revenue_by_customer(SALES) == {"c1": 150.0, "c2": 50.0}


def test_top_customers():
    assert top_customers(SALES, 2) == [("c1", 150.0), ("c2", 50.0)]
    assert top_customers(SALES, 1) == [("c1", 150.0)]


def test_top_customers_ties():
    sales = [
        Sale(region="QLD", amount=50.0, completed=True, customer_id="c2"),
        Sale(region="NSW", amount=50.0, completed=True, customer_id="c1"),
    ]
    assert top_customers(sales, 2) == [("c1", 50.0), ("c2", 50.0)]


def test_revenue_share_by_region():
    shares = revenue_share_by_region(SALES)
    assert shares == {"QLD": 0.75, "NSW": 0.25}
    assert sum(shares.values()) == 1.0


def test_revenue_share_by_region_zero_total():
    sales = [Sale(region="QLD", amount=None, completed=True)]
    assert revenue_share_by_region(sales) == {}
