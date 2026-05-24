from src.interfaces.notifier import INotifier
from src.interfaces.order_event_observer import IOrderEventObserver


class EmailOrderObserver(IOrderEventObserver):
    """Envia email para todos os eventos de pedido."""

    def __init__(self, notifier: INotifier) -> None:
        self._notifier = notifier

    def on_order_received(self, client: str, client_type: str) -> None:
        self._notifier.send_email(client, "Pedido recebido!")

    def on_order_approved(self, client: str, client_type: str) -> None:
        self._notifier.send_email(client, "Pedido aprovado!")

    def on_order_sent(self, client: str) -> None:
        self._notifier.send_email(client, "Pedido enviado!")

    def on_order_delivered(
        self, client: str, client_type: str, total: float
    ) -> None:
        self._notifier.send_email(client, "Pedido entregue!")


class SmsOrderObserver(IOrderEventObserver):
    """Envia SMS para clientes VIP nos eventos de recebimento e aprovação."""

    def __init__(self, notifier: INotifier) -> None:
        self._notifier = notifier

    def on_order_received(self, client: str, client_type: str) -> None:
        if client_type == "vip":
            self._notifier.send_sms(client, "Pedido VIP recebido!")

    def on_order_approved(self, client: str, client_type: str) -> None:
        if client_type == "vip":
            self._notifier.send_sms(client, "Pedido aprovado!")

    def on_order_sent(self, client: str) -> None:
        pass

    def on_order_delivered(
        self, client: str, client_type: str, total: float
    ) -> None:
        pass


class AccountManagerOrderObserver(IOrderEventObserver):
    """Notifica o gerente de conta para clientes corporativos ao receber pedido."""

    def __init__(self, notifier: INotifier) -> None:
        self._notifier = notifier

    def on_order_received(self, client: str, client_type: str) -> None:
        if client_type == "corporativo":
            self._notifier.notify_account_manager(client)

    def on_order_approved(self, client: str, client_type: str) -> None:
        pass

    def on_order_sent(self, client: str) -> None:
        pass

    def on_order_delivered(
        self, client: str, client_type: str, total: float
    ) -> None:
        pass


class PointsOrderObserver(IOrderEventObserver):
    """Calcula e exibe pontos de fidelidade quando o pedido é entregue."""

    def on_order_received(self, client: str, client_type: str) -> None:
        pass

    def on_order_approved(self, client: str, client_type: str) -> None:
        pass

    def on_order_sent(self, client: str) -> None:
        pass

    def on_order_delivered(
        self, client: str, client_type: str, total: float
    ) -> None:
        if client_type == "vip":
            points = int(total * 2)
            print(f"Cliente VIP ganhou {points} pontos!")
        elif client_type == "corporativo":
            points = int(total * 1.5)
            print(f"Cliente corporativo ganhou {points} pontos!")
        else:
            points = int(total)
            print(f"Cliente ganhou {points} pontos!")
