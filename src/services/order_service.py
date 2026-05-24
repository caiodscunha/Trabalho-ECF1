from datetime import datetime
from typing import Any, Optional

from src.interfaces.discount_strategy import IClientDiscountStrategy, IItemPriceCalculator
from src.interfaces.order_repository import IOrderRepository
from src.models.order import Order
from src.services.notification_service import NotificationService
from src.strategies.discount_strategy import (
    DefaultItemPriceCalculator,
    NoClientDiscount,
    _DEFAULT_CLIENT_DISCOUNTS,
)


class OrderService:
    """Orquestra o ciclo de vida do pedido.

    OCP: IItemPriceCalculator é injetável — decorar com novas regras de
    desconto (ex: volume) sem modificar esta classe.
    DIP: depende apenas de abstrações (IOrderRepository, IItemPriceCalculator,
    IClientDiscountStrategy).
    """

    def __init__(
        self,
        repository: IOrderRepository,
        notification_service: NotificationService,
        item_calculator: Optional[IItemPriceCalculator] = None,
        client_discounts: Optional[dict[str, IClientDiscountStrategy]] = None,
    ) -> None:
        self._repository = repository
        self._notifications = notification_service
        self._item_calculator = item_calculator or DefaultItemPriceCalculator()
        self._client_discounts = client_discounts if client_discounts is not None else _DEFAULT_CLIENT_DISCOUNTS

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
        subtotal = sum(self._item_calculator.calculate(item) for item in items)
        discount = self._client_discounts.get(client_type, NoClientDiscount())
        return discount.apply(subtotal)

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
