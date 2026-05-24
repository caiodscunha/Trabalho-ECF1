from typing import Optional

from src.interfaces.order_repository import IOrderRepository
from src.interfaces.payment_strategy import IPaymentStrategy
from src.services.notification_service import NotificationService
from src.strategies.payment_strategy import BoletoStrategy, CartaoStrategy, PixStrategy

_DEFAULT_STRATEGIES: dict[str, IPaymentStrategy] = {
    "cartao": CartaoStrategy(),
    "pix": PixStrategy(),
    "boleto": BoletoStrategy(),
}


class PaymentService:
    """Processa pagamentos delegando a lógica de cada método a uma Strategy.

    OCP: adicionar novo método = criar nova IPaymentStrategy, registrar no
    dicionário. PaymentService nunca precisa ser modificado.
    DIP: depende de IOrderRepository e IPaymentStrategy (abstrações).
    """

    def __init__(
        self,
        repository: IOrderRepository,
        notification_service: NotificationService,
        strategies: Optional[dict[str, IPaymentStrategy]] = None,
    ) -> None:
        self._repository = repository
        self._notifications = notification_service
        self._strategies = strategies if strategies is not None else _DEFAULT_STRATEGIES

    def process_payment(self, order_id: int, method: str, value: float) -> bool:
        order = self._repository.get_by_id(order_id)
        if order is None:
            return False

        strategy = self._strategies.get(method)
        if strategy is None:
            print("Metodo de pagamento invalido!")
            return False

        if value < strategy.required_amount(order.total):
            print("Valor insuficiente!")
            return False

        success = strategy.process()
        if success and strategy.auto_approves:
            self._approve(order_id, order.cliente, order.tipo_cliente)
        return success

    def _approve(self, order_id: int, client: str, client_type: str) -> None:
        self._repository.update_status(order_id, "aprovado")
        self._notifications.notify_order_approved(client, client_type)
