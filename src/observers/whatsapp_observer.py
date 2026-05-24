from src.interfaces.order_event_observer import IOrderEventObserver


class WhatsAppOrderObserver(IOrderEventObserver):
    """Envia notificacoes via WhatsApp para todos os tipos de cliente.

    OCP: classe nova, nenhuma existente modificada. Basta fazer subscribe()
    no NotificationService para ativar o canal WhatsApp.
    """

    def __init__(self, recipient: str) -> None:
        self._recipient = recipient

    def on_order_received(self, client: str, client_type: str) -> None:
        print(f"WhatsApp enviado para {client}: Pedido recebido!")

    def on_order_approved(self, client: str, client_type: str) -> None:
        print(f"WhatsApp enviado para {client}: Pedido aprovado!")

    def on_order_sent(self, client: str) -> None:
        print(f"WhatsApp enviado para {client}: Pedido enviado!")

    def on_order_delivered(
        self, client: str, client_type: str, total: float
    ) -> None:
        print(f"WhatsApp enviado para {client}: Pedido entregue!")
