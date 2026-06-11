from __future__ import annotations

from src.filters import included_sales
from src.types import Region, Sale


def total_revenue(sales: list[Sale]) -> float:
    return float(sum(s.amount for s in included_sales(sales)))


def revenue_by_region(sales: list[Sale]) -> dict[Region, float]:
    revenue: dict[Region, float] = {}
    for sale in included_sales(sales):
        revenue[sale.region] = revenue.get(sale.region, 0.0) + sale.amount
    return revenue


def average_sale(sales: list[Sale]) -> float:
    included = included_sales(sales)
    if not included:
        return 0.0
    return sum(s.amount for s in included) / len(included)


def sale_count_by_region(sales: list[Sale]) -> dict[Region, int]:
    counts: dict[Region, int] = {}
    for sale in included_sales(sales):
        counts[sale.region] = counts.get(sale.region, 0) + 1
    return counts


def revenue_by_customer(sales: list[Sale]) -> dict[str, float]:
    revenue: dict[str, float] = {}
    for sale in included_sales(sales):
        revenue[sale.customer_id] = revenue.get(sale.customer_id, 0.0) + sale.amount
    return revenue


def top_customers(sales: list[Sale], n: int) -> list[tuple[str, float]]:
    revenue = revenue_by_customer(sales)
    ranked = sorted(revenue.items(), key=lambda item: (-item[1], item[0]))
    return ranked[:n]


def revenue_share_by_region(sales: list[Sale]) -> dict[Region, float]:
    total = total_revenue(sales)
    if total == 0:
        return {}
    return {region: revenue / total for region, revenue in revenue_by_region(sales).items()}
