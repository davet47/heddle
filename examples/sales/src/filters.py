from __future__ import annotations

from src.types import Region, Sale


def included_sales(sales: list[Sale]) -> list[Sale]:
    return [s for s in sales if s.completed and s.amount is not None]


def sales_in_region(sales: list[Sale], region: Region) -> list[Sale]:
    return [s for s in included_sales(sales) if s.region == region]


def sales_over(sales: list[Sale], threshold: float) -> list[Sale]:
    return [s for s in included_sales(sales) if s.amount > threshold]
