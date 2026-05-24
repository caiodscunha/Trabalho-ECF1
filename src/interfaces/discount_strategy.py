from abc import ABC, abstractmethod
from typing import Any


class IItemPriceCalculator(ABC):
    """Contrato para cálculo do subtotal de um item (Strategy GoF).

    Encapsula o algoritmo de precificação por item. Decorar com novas regras
    (ex: desconto por volume) sem modificar implementações existentes.
    """

    @abstractmethod
    def calculate(self, item: dict[str, Any]) -> float:
        """Retorna o subtotal do item após aplicar desconto."""


class IClientDiscountStrategy(ABC):
    """Contrato para desconto aplicado ao total do pedido por tipo de cliente."""

    @abstractmethod
    def apply(self, total: float) -> float:
        """Retorna o total após aplicar o desconto do cliente."""
