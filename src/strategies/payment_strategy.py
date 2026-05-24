from src.interfaces.payment_strategy import IPaymentStrategy


class CartaoStrategy(IPaymentStrategy):
    def process(self) -> bool:
        print("Processando pagamento com cartao...")
        print("Cartao validado!")
        return True


class PixStrategy(IPaymentStrategy):
    def process(self) -> bool:
        print("Gerando QR Code PIX...")
        print("PIX recebido!")
        return True


class BoletoStrategy(IPaymentStrategy):
    @property
    def auto_approves(self) -> bool:
        return False

    def process(self) -> bool:
        print("Gerando boleto...")
        print("Boleto gerado!")
        return True
