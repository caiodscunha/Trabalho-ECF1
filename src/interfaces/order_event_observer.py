from abc import ABC, abstractmethod


class IOrderEventObserver(ABC):
    """Contrato para observadores de eventos de pedido (Observer GoF).

    NotificationService é o Subject. Cada canal (email, SMS, WhatsApp) é um
    Observer concreto. Adicionar canal = nova classe, sem tocar no Subject.
    """

    @abstractmethod
    def on_order_received(self, client: str, client_type: str) -> None:
        """Disparado quando um novo pedido é criado."""

    @abstractmethod
    def on_order_approved(self, client: str, client_type: str) -> None:
        """Disparado quando o pagamento aprova o pedido."""

    @abstractmethod
    def on_order_sent(self, client: str) -> None:
        """Disparado quando o pedido é enviado."""

    @abstractmethod
    def on_order_delivered(
        self, client: str, client_type: str, total: float
    ) -> None:
        """Disparado quando o pedido é entregue."""
