from abc import ABC, abstractmethod
from typing import Optional

from src.models.order import Order


class IOrderRepository(ABC):
    """Contrato para acesso à persistência de pedidos.

    Define apenas as operações que os serviços precisam — em conformidade
    com ISP. A implementação concreta (SQLite, em memória, etc.) fica em
    ``repositories``.
    """

    @abstractmethod
    def add(self, order: Order) -> int:
        """Persiste o pedido e devolve o id gerado."""

    @abstractmethod
    def get_by_id(self, order_id: int) -> Optional[Order]:
        """Recupera o pedido pelo id, ou None se não existir."""

    @abstractmethod
    def update_status(self, order_id: int, status: str) -> None:
        """Atualiza o campo status do pedido."""

    @abstractmethod
    def list_all(self) -> list[Order]:
        """Lista todos os pedidos persistidos."""

    @abstractmethod
    def list_distinct_clients(self) -> list[tuple[str, str]]:
        """Lista pares (cliente, tipo_cliente) distintos."""

    @abstractmethod
    def sum_total_by_client(self, client: str) -> float:
        """Soma os totais de todos os pedidos do cliente."""

    @abstractmethod
    def close(self) -> None:
        """Libera os recursos da conexão."""
