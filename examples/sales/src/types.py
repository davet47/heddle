from __future__ import annotations

from dataclasses import dataclass

Region = str


@dataclass
class Sale:
    region: Region
    amount: float | None
    completed: bool
    customer_id: str = ""
    product_id: str = ""


@dataclass
class Customer:
    id: str
    name: str
    segment: str


@dataclass
class Product:
    id: str
    name: str
    category: str
