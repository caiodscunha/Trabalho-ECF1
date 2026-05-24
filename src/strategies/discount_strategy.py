from typing import Any

from src.interfaces.discount_strategy import IClientDiscountStrategy, IItemPriceCalculator

_ITEM_FACTORS: dict[str, float] = {
    "normal": 1.0,
    "frete_gratis": 1.0,
    "desc10": 0.9,
    "desc20": 0.8,
}


class DefaultItemPriceCalculator(IItemPriceCalculator):
    """Calcula subtotal aplicando o fator de desconto por tipo de item."""

    def calculate(self, item: dict[str, Any]) -> float:
        base = item["p"] * item["q"]
        return base * _ITEM_FACTORS.get(item["tipo"], 0.0)


class VipClientDiscount(IClientDiscountStrategy):
    def apply(self, total: float) -> float:
        return total * 0.95


class CorporativoClientDiscount(IClientDiscountStrategy):
    def apply(self, total: float) -> float:
        return total * 0.90


class NoClientDiscount(IClientDiscountStrategy):
    def apply(self, total: float) -> float:
        return total


_DEFAULT_CLIENT_DISCOUNTS: dict[str, IClientDiscountStrategy] = {
    "vip": VipClientDiscount(),
    "corporativo": CorporativoClientDiscount(),
}
