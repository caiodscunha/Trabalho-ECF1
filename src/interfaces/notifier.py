from abc import ABC, abstractmethod


class INotifier(ABC):
    """Contrato para canais externos de notificação.

    Mantém regra de negócio independente do meio (email, SMS, mensageria).
    Em Sprint 2, esta ABC vai casar com o padrão Observer.
    """

    @abstractmethod
    def send_email(self, recipient: str, message: str) -> None:
        """Envia mensagem por email."""

    @abstractmethod
    def send_sms(self, recipient: str, message: str) -> None:
        """Envia mensagem por SMS."""

    @abstractmethod
    def notify_account_manager(self, client: str) -> None:
        """Aciona o gerente de conta vinculado ao cliente."""
