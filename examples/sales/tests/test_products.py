from src.products import revenue_by_category, revenue_by_product, top_products
from src.types import Product, Sale

PRODUCTS = [
    Product(id="p1", name="Widget", category="hardware"),
    Product(id="p2", name="Gadget", category="hardware"),
    Product(id="p3", name="Course", category="services"),
]

SALES = [
    Sale(region="QLD", amount=100.0, completed=True, product_id="p1"),
    Sale(region="NSW", amount=40.0, completed=True, product_id="p2"),
    Sale(region="NSW", amount=60.0, completed=True, product_id="p3"),
    Sale(region="VIC", amount=999.0, completed=True, product_id="px"),
    Sale(region="VIC", amount=None, completed=True, product_id="p1"),
    Sale(region="VIC", amount=10.0, completed=False, product_id="p1"),
]


def test_revenue_by_product():
    assert revenue_by_product(SALES, PRODUCTS) == {"p1": 100.0, "p2": 40.0, "p3": 60.0}


def test_revenue_by_category():
    assert revenue_by_category(SALES, PRODUCTS) == {"hardware": 140.0, "services": 60.0}


def test_top_products():
    assert top_products(SALES, PRODUCTS, 2) == [("p1", 100.0), ("p3", 60.0)]


def test_top_products_ties():
    sales = [
        Sale(region="QLD", amount=50.0, completed=True, product_id="p2"),
        Sale(region="QLD", amount=50.0, completed=True, product_id="p1"),
    ]
    assert top_products(sales, PRODUCTS, 2) == [("p1", 50.0), ("p2", 50.0)]
