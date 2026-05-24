"""Testes da extensão: pagamento em criptomoeda (taxa de 2%).

OCP verificado: apenas src/strategies/crypto_payment_strategy.py foi adicionado.
Nenhuma classe existente foi modificada para habilitar este método de pagamento.
"""
import pytest

from src.repositories.sqlite_order_repository import SqliteOrderRepository
from src.observers.notification_observer import EmailOrderObserver
from src.services.notification_service import ConsoleNotifier, NotificationService
from src.services.payment_service import PaymentService
from src.strategies.crypto_payment_strategy import CryptoPaymentStrategy


@pytest.fixture
def payment_service(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    repo = SqliteOrderRepository("loja.db")
    notifications = NotificationService()
    notifications.subscribe(EmailOrderObserver(ConsoleNotifier()))
    strategies = {"cripto": CryptoPaymentStrategy()}
    service = PaymentService(repo, notifications, strategies)
    yield service, repo
    repo.close()


def _create_order(repo, total: float) -> int:
    from datetime import datetime
    from src.models.order import Order
    order = Order(
        cliente="Cliente",
        itens=[],
        total=total,
        status="pendente",
        data=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        tipo_cliente="normal",
    )
    return repo.add(order)


def test_cripto_exige_taxa_de_2_por_cento(payment_service):
    service, repo = payment_service
    order_id = _create_order(repo, 100.0)
    # Valor exato do pedido não é suficiente — precisa pagar a taxa
    result = service.process_payment(order_id, "cripto", 100.0)
    assert result is False


def test_cripto_aceita_com_taxa(payment_service):
    service, repo = payment_service
    order_id = _create_order(repo, 100.0)
    # 100 * 1.02 = 102
    result = service.process_payment(order_id, "cripto", 102.0)
    assert result is True


def test_cripto_aprova_pedido_automaticamente(payment_service):
    service, repo = payment_service
    order_id = _create_order(repo, 100.0)
    service.process_payment(order_id, "cripto", 102.0)
    order = repo.get_by_id(order_id)
    assert order is not None
    assert order.status == "aprovado"


def test_cripto_taxa_calculada_sobre_total_do_pedido(payment_service):
    service, repo = payment_service
    order_id = _create_order(repo, 200.0)
    # 200 * 1.02 = 204 — valor exato passa
    result = service.process_payment(order_id, "cripto", 204.0)
    assert result is True
