from __future__ import annotations

from src.filters import included_sales
from src.types import Product, Sale


def revenue_by_product(sales: list[Sale], products: list[Product]) -> dict[str, float]:
    known_ids = {p.id for p in products}
    revenue: dict[str, float] = {}
    for sale in included_sales(sales):
        if sale.product_id in known_ids:
            revenue[sale.product_id] = revenue.get(sale.product_id, 0.0) + sale.amount
    return revenue


def revenue_by_category(sales: list[Sale], products: list[Product]) -> dict[str, float]:
    category_of = {p.id: p.category for p in products}
    revenue: dict[str, float] = {}
    for product_id, amount in revenue_by_product(sales, products).items():
        category = category_of[product_id]
        revenue[category] = revenue.get(category, 0.0) + amount
    return revenue


def top_products(sales: list[Sale], products: list[Product], n: int) -> list[tuple[str, float]]:
    revenue = revenue_by_product(sales, products)
    ranked = sorted(revenue.items(), key=lambda item: (-item[1], item[0]))
    return ranked[:n]
