from src.types import Customer, Product, Sale


def test_sale_constructor():
    sale = Sale(region="QLD", amount=10.0, completed=True)
    assert sale.region == "QLD"
    assert sale.amount == 10.0
    assert sale.completed is True
    assert sale.customer_id == ""
    assert sale.product_id == ""


def test_customer_constructor():
    customer = Customer(id="c1", name="Acme Pty Ltd", segment="enterprise")
    assert (customer.id, customer.name, customer.segment) == ("c1", "Acme Pty Ltd", "enterprise")


def test_product_constructor():
    product = Product(id="p1", name="Widget", category="hardware")
    assert (product.id, product.name, product.category) == ("p1", "Widget", "hardware")
