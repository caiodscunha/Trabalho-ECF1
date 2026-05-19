from abc import ABC, abstractmethod


class IInventoryProvider(ABC):
    """Contrato para o sistema externo de estoque.

    No legado o estoque vive embutido no método ``validar_estoque``. Isolando
    em ABC, fica trivial trocar por uma integração HTTP real depois.
    """

    @abstractmethod
    def product_exists(self, product_name: str) -> bool:
        """Indica se o produto está cadastrado no estoque."""

    @abstractmethod
    def has_stock(self, product_name: str, quantity: int) -> bool:
        """Indica se há estoque suficiente para a quantidade pedida."""
