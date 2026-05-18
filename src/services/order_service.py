from datetime import datetime
from typing import Any, Optional

from src.interfaces.order_repository import IOrderRepository
from src.models.order import Order
from src.services.notification_service import NotificationService


class OrderService:
    """Orquestra o ciclo de vida do pedido: criação, transição de status,
    cancelamento e consultas agregadas por cliente.

    SRP: regra de negócio do pedido. Persistência fica no repository e
    notificação fica no NotificationService — ambos injetados.

    As cadeias de if/elif por tipo de cliente/item permanecem aqui em
    Sprint 1; serão substituídas por Strategy em Sprint 2 (OCP).
    """

    _DISCOUNT_BY_CLIENT_TYPE = {
        "vip": 0.95,
        "corporativo": 0.90,
    }

    def __init__(
        self,
        repository: IOrderRepository,
        notification_service: NotificationService,
    ) -> None:
        self._repository = repository
        self._notifications = notification_service

    def create_order(
        self, client: str, items: list[dict[str, Any]], client_type: str
    ) -> int:
        total = self._calculate_total(items, client_type)
        order = Order(
            cliente=client,
            itens=items,
            total=total,
            status="pendente",
            data=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            tipo_cliente=client_type,
        )
        order_id = self._repository.add(order)
        self._notifications.notify_order_received(client, client_type)
        return order_id

    def update_status(self, order_id: int, new_status: str) -> None:
        order = self._repository.get_by_id(order_id)
        if order is None:
            return
        self._repository.update_status(order_id, new_status)
        self._notify_status_change(order, new_status)

    def cancel_order(self, order_id: int) -> None:
        self._repository.update_status(order_id, "cancelado")
        print(f"Pedido {order_id} cancelado")

    def get_order(self, order_id: int) -> Optional[Order]:
        return self._repository.get_by_id(order_id)

    def total_for_client(self, client: str) -> float:
        return self._repository.sum_total_by_client(client)

    def _calculate_total(
        self, items: list[dict[str, Any]], client_type: str
    ) -> float:
        total = 0.0
        for item in items:
            total += self._apply_item_discount(item)
        return total * self._DISCOUNT_BY_CLIENT_TYPE.get(client_type, 1.0)

    @staticmethod
    def _apply_item_discount(item: dict[str, Any]) -> float:
        base = item["p"] * item["q"]
        tipo = item["tipo"]
        if tipo == "normal" or tipo == "frete_gratis":
            return base
        if tipo == "desc10":
            return base * 0.9
        if tipo == "desc20":
            return base * 0.8
        return 0.0

    def _notify_status_change(self, order: Order, new_status: str) -> None:
        if new_status == "aprovado":
            self._notifications.notify_order_approved(
                order.cliente, order.tipo_cliente
            )
        elif new_status == "enviado":
            self._notifications.notify_order_sent(order.cliente)
        elif new_status == "entregue":
            self._notifications.notify_order_delivered(
                order.cliente, order.tipo_cliente, order.total
            )
