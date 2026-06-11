from __future__ import annotations

from src.metrics import revenue_by_customer, total_revenue
from src.types import Customer, Sale


def customers_by_segment(customers: list[Customer]) -> dict[str, list[Customer]]:
    grouped: dict[str, list[Customer]] = {}
    for customer in customers:
        grouped.setdefault(customer.segment, []).append(customer)
    return grouped


def revenue_by_segment(sales: list[Sale], customers: list[Customer]) -> dict[str, float]:
    customer_revenue = revenue_by_customer(sales)
    revenue: dict[str, float] = {}
    for segment, members in customers_by_segment(customers).items():
        revenue[segment] = sum(customer_revenue.get(c.id, 0.0) for c in members)
    return revenue


def segment_revenue_share(sales: list[Sale], customers: list[Customer]) -> dict[str, float]:
    total = total_revenue(sales)
    if total == 0:
        return {}
    return {
        segment: revenue / total
        for segment, revenue in revenue_by_segment(sales, customers).items()
    }
