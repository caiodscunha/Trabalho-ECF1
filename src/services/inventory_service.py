from typing import Any

from src.interfaces.inventory import IInventoryProvider


class StaticInventoryProvider(IInventoryProvider):
    """Provedor de estoque com tabela fixa em memória.

    Substitui o dicionário hardcoded que estava dentro de Sis.validar_estoque.
    Em produção esta classe seria trocada por uma integração HTTP real.
    """

    _STOCK = {"produto1": 100, "produto2": 50, "produto3": 75}

    def product_exists(self, product_name: str) -> bool:
        return product_name in self._STOCK

    def has_stock(self, product_name: str, quantity: int) -> bool:
        return self._STOCK.get(product_name, 0) >= quantity


class InventoryService:
    """Valida disponibilidade de estoque para uma lista de itens de pedido."""

    def __init__(self, inventory_provider: IInventoryProvider) -> None:
        self._provider = inventory_provider

    def validate(self, items: list[dict[str, Any]]) -> bool:
        for item in items:
            name = item["nome"]
            if not self._provider.product_exists(name):
                print(f"Produto {name} nao encontrado!")
                return False
            if not self._provider.has_stock(name, item["q"]):
                print(f"Estoque insuficiente para {name}!")
                return False
        return True
