import json
from datetime import datetime
from typing import Any

from src.interfaces.order_factory import IOrderFactory
from src.interfaces.order_repository import IOrderRepository
from src.models.order import Order
from src.services.order_service import OrderService

_SPECIAL_ITEM_FACTORS: dict[str, float] = {
    "normal": 1.0,
    "desc10": 0.9,
    "desc20": 0.8,
}


class StandardOrderFactory(IOrderFactory):
    """Delega criação de pedidos normais/vip/corporativo ao OrderService."""

    def __init__(self, order_service: OrderService) -> None:
        self._order_service = order_service

    def create(
        self, client: str, items: list[dict[str, Any]], client_type: str
    ) -> int:
        return self._order_service.create_order(client, items, client_type)


class SpecialOrderFactory(IOrderFactory):
    """Cria pedidos com taxa especial de 15% (comportamento de PedEspecial).

    LSP: a lógica especial agora vive em composição, não em herança.
    PedEspecial deixa de estender Sis — usa esta factory internamente.
    A multiplicação por 1.15 é aplicada dentro do loop por item para preservar
    o comportamento exato do sistema legado.
    """

    def __init__(self, repository: IOrderRepository) -> None:
        self._repository = repository

    def create(
        self, client: str, items: list[dict[str, Any]], client_type: str
    ) -> int:
        total = self._calculate_special_total(items)
        order = Order(
            cliente=client,
            itens=items,
            total=total,
            status="pendente",
            data=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            tipo_cliente=client_type,
        )
        order_id = self._repository.add(order)
        print(f"Email especial enviado para {client}: Pedido especial recebido!")
        return order_id

    @staticmethod
    def _calculate_special_total(items: list[dict[str, Any]]) -> float:
        tot: float = 0.0
        for item in items:
            factor = _SPECIAL_ITEM_FACTORS.get(item["tipo"], 0.0)
            tot += item["p"] * item["q"] * factor
            tot = tot * 1.15
        return tot
