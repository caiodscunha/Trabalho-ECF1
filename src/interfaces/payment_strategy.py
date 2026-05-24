from abc import ABC, abstractmethod


class IPaymentStrategy(ABC):
    """Contrato para algoritmos de processamento de pagamento (Strategy GoF).

    Cada método de pagamento encapsula sua lógica própria. Adicionar um novo
    método = criar nova classe concreta, sem modificar PaymentService.
    """

    def required_amount(self, order_total: float) -> float:
        """Valor mínimo exigido para aceitar o pagamento.

        Por padrão é o total do pedido. Estratégias com taxa (ex: cripto)
        sobrescrevem para adicionar a cobrança extra.
        """
        return order_total

    @abstractmethod
    def process(self) -> bool:
        """Executa o processamento do pagamento. Retorna True se aceito."""

    @property
    def auto_approves(self) -> bool:
        """True se a aprovação do pedido ocorre automaticamente.

        Boleto não aprova; cartão e PIX aprovam. Novas estratégias sobrescrevem.
        """
        return True
