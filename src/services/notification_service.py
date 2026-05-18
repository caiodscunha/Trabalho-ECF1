from src.interfaces.notifier import INotifier


class ConsoleNotifier(INotifier):
    """Notifier concreto que escreve no console.

    Preserva o comportamento do legado (todos os "envios" são prints), mas
    isolado atrás da ABC INotifier para troca futura sem mexer em regras.
    """

    def send_email(self, recipient: str, message: str) -> None:
        print(f"Email enviado para {recipient}: {message}")

    def send_sms(self, recipient: str, message: str) -> None:
        print(f"SMS enviado para {recipient}: {message}")

    def notify_account_manager(self, client: str) -> None:
        print(f"Notificacao enviada ao gerente de conta de {client}")


class NotificationService:
    """Coordena que notificações disparar para cada evento e tipo de cliente.

    SRP: única responsabilidade é decidir e disparar notificações.
    Não conhece persistência nem cálculos de pedido.
    """

    def __init__(self, notifier: INotifier) -> None:
        self._notifier = notifier

    def notify_order_received(self, client: str, client_type: str) -> None:
        if client_type == "normal":
            self._notifier.send_email(client, "Pedido recebido!")
        elif client_type == "vip":
            self._notifier.send_email(client, "Pedido recebido!")
            self._notifier.send_sms(client, "Pedido VIP recebido!")
        elif client_type == "corporativo":
            self._notifier.send_email(client, "Pedido recebido!")
            self._notifier.notify_account_manager(client)

    def notify_order_approved(self, client: str, client_type: str) -> None:
        self._notifier.send_email(client, "Pedido aprovado!")
        if client_type == "vip":
            self._notifier.send_sms(client, "Pedido aprovado!")

    def notify_order_sent(self, client: str) -> None:
        self._notifier.send_email(client, "Pedido enviado!")

    def notify_order_delivered(
        self, client: str, client_type: str, total: float
    ) -> None:
        self._notifier.send_email(client, "Pedido entregue!")
        if client_type == "vip":
            points = int(total * 2)
            print(f"Cliente VIP ganhou {points} pontos!")
        elif client_type == "corporativo":
            points = int(total * 1.5)
            print(f"Cliente corporativo ganhou {points} pontos!")
        else:
            points = int(total)
            print(f"Cliente ganhou {points} pontos!")
