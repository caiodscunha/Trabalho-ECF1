from abc import ABC, abstractmethod
from typing import Any


class IOrderFactory(ABC):
    """Contrato para criação de pedidos (Factory Method GoF).

    Desacopla a lógica de criação do tipo concreto de pedido. Adicionar um
    novo tipo (especial, urgente) = nova fábrica concreta, sem alterar clientes.
    """

    @abstractmethod
    def create(
        self, client: str, items: list[dict[str, Any]], client_type: str
    ) -> int:
        """Cria o pedido e retorna o id gerado."""
