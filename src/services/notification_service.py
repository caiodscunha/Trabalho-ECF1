from src.interfaces.notifier import INotifier
from src.interfaces.order_event_observer import IOrderEventObserver


class ConsoleNotifier(INotifier):
    """Notifier concreto que escreve no console."""

    def send_email(self, recipient: str, message: str) -> None:
        print(f"Email enviado para {recipient}: {message}")

    def send_sms(self, recipient: str, message: str) -> None:
        print(f"SMS enviado para {recipient}: {message}")

    def notify_account_manager(self, client: str) -> None:
        print(f"Notificacao enviada ao gerente de conta de {client}")


class NotificationService:
    """Subject do padrão Observer para eventos de pedido (Observer GoF).

    Mantém lista de IOrderEventObserver e os notifica a cada evento.
    OCP: adicionar canal (WhatsApp, push) = criar novo observer e registrá-lo
    via subscribe() — NotificationService nunca precisa ser modificado.
    """

    def __init__(self) -> None:
        self._observers: list[IOrderEventObserver] = []

    def subscribe(self, observer: IOrderEventObserver) -> None:
        self._observers.append(observer)

    def notify_order_received(self, client: str, client_type: str) -> None:
        for obs in self._observers:
            obs.on_order_received(client, client_type)

    def notify_order_approved(self, client: str, client_type: str) -> None:
        for obs in self._observers:
            obs.on_order_approved(client, client_type)

    def notify_order_sent(self, client: str) -> None:
        for obs in self._observers:
            obs.on_order_sent(client)

    def notify_order_delivered(
        self, client: str, client_type: str, total: float
    ) -> None:
        for obs in self._observers:
            obs.on_order_delivered(client, client_type, total)
