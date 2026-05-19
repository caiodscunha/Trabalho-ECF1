from src.interfaces.order_repository import IOrderRepository
from src.services.notification_service import NotificationService


class PaymentService:
    """Processa pagamentos e dispara a aprovação quando cabível.

    SRP: regra de pagamento e seu efeito no status. O 'como' notificar e o
    'como' persistir são delegados aos colaboradores recebidos no construtor.
    A cadeia de if/elif para método de pagamento será substituída por Strategy
    em Sprint 2 (OCP).
    """

    def __init__(
        self,
        repository: IOrderRepository,
        notification_service: NotificationService,
    ) -> None:
        self._repository = repository
        self._notifications = notification_service

    def process_payment(self, order_id: int, method: str, value: float) -> bool:
        order = self._repository.get_by_id(order_id)
        if order is None:
            return False
        if value < order.total:
            print("Valor insuficiente!")
            return False

        if method == "cartao":
            print("Processando pagamento com cartao...")
            print("Cartao validado!")
            self._approve(order_id, order.cliente, order.tipo_cliente)
            return True
        if method == "pix":
            print("Gerando QR Code PIX...")
            print("PIX recebido!")
            self._approve(order_id, order.cliente, order.tipo_cliente)
            return True
        if method == "boleto":
            print("Gerando boleto...")
            print("Boleto gerado!")
            return True

        print("Metodo de pagamento invalido!")
        return False

    def _approve(self, order_id: int, client: str, client_type: str) -> None:
        self._repository.update_status(order_id, "aprovado")
        self._notifications.notify_order_approved(client, client_type)
