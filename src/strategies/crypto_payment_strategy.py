from src.interfaces.payment_strategy import IPaymentStrategy

_FEE_RATE = 0.02


class CryptoPaymentStrategy(IPaymentStrategy):
    """Pagamento em criptomoeda com taxa de 2% sobre o valor do pedido.

    OCP: classe nova, nenhuma existente modificada. Basta registrar no dict de
    strategies do PaymentService para ativar o método 'cripto'.
    """

    def required_amount(self, order_total: float) -> float:
        return order_total * (1 + _FEE_RATE)

    def process(self) -> bool:
        print("Processando pagamento em criptomoeda...")
        print("Transacao de cripto confirmada!")
        return True
