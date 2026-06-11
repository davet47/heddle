from src.customers import customers_by_segment, revenue_by_segment, segment_revenue_share
from src.types import Customer, Sale

CUSTOMERS = [
    Customer(id="c1", name="Acme Pty Ltd", segment="enterprise"),
    Customer(id="c2", name="Bolt Co", segment="smb"),
    Customer(id="c3", name="Crux Group", segment="enterprise"),
]

SALES = [
    Sale(region="QLD", amount=80.0, completed=True, customer_id="c1"),
    Sale(region="NSW", amount=20.0, completed=True, customer_id="c2"),
    Sale(region="VIC", amount=None, completed=True, customer_id="c3"),
    Sale(region="VIC", amount=50.0, completed=False, customer_id="c3"),
]


def test_customers_by_segment():
    grouped = customers_by_segment(CUSTOMERS)
    assert grouped == {
        "enterprise": [CUSTOMERS[0], CUSTOMERS[2]],
        "smb": [CUSTOMERS[1]],
    }


def test_revenue_by_segment():
    assert revenue_by_segment(SALES, CUSTOMERS) == {"enterprise": 80.0, "smb": 20.0}


def test_segment_revenue_share():
    assert segment_revenue_share(SALES, CUSTOMERS) == {"enterprise": 0.8, "smb": 0.2}


def test_segment_revenue_share_zero_total():
    sales = [Sale(region="QLD", amount=None, completed=True, customer_id="c1")]
    assert segment_revenue_share(sales, CUSTOMERS) == {}
