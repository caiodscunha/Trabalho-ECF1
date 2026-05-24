from typing import Any

from src.interfaces.discount_strategy import IItemPriceCalculator

_THRESHOLD = 3
_DISCOUNT_RATE = 0.85


class VolumeDiscountCalculator(IItemPriceCalculator):
    """Desconto progressivo: 3+ unidades do mesmo item recebem 15% adicional.

    OCP: decora IItemPriceCalculator existente (Decorator GoF). Nenhuma classe
    existente foi modificada. Injetar no OrderService ativa a regra.
    """

    def __init__(self, base: IItemPriceCalculator) -> None:
        self._base = base

    def calculate(self, item: dict[str, Any]) -> float:
        subtotal = self._base.calculate(item)
        if item["q"] >= _THRESHOLD:
            return subtotal * _DISCOUNT_RATE
        return subtotal
