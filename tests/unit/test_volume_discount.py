"""Testes da extensao: desconto progressivo por volume (3+ unidades = 15% off).

OCP verificado: apenas VolumeDiscountCalculator adicionado, nenhuma classe
existente modificada. Injetar no OrderService ativa a regra de volume.
"""
import pytest

from src.observers.notification_observer import EmailOrderObserver
from src.repositories.sqlite_order_repository import SqliteOrderRepository
from src.services.notification_service import ConsoleNotifier, NotificationService
from src.services.order_service import OrderService
from src.strategies.discount_strategy import DefaultItemPriceCalculator
from src.strategies.volume_discount_strategy import VolumeDiscountCalculator


@pytest.fixture
def order_service(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    repo = SqliteOrderRepository("loja.db")
    notifications = NotificationService()
    notifications.subscribe(EmailOrderObserver(ConsoleNotifier()))
    calculator = VolumeDiscountCalculator(DefaultItemPriceCalculator())
    service = OrderService(repo, notifications, item_calculator=calculator)
    yield service, repo
    repo.close()


def test_desconto_volume_aplica_15_porcento_com_3_unidades(order_service):
    service, repo = order_service
    items = [{"nome": "p1", "p": 100, "q": 3, "tipo": "normal"}]
    order_id = service.create_order("Cliente", items, "normal")
    order = repo.get_by_id(order_id)
    # 100 * 3 = 300, com 15% off = 255
    assert order is not None
    assert order.total == pytest.approx(255.0)


def test_desconto_volume_nao_aplica_com_menos_de_3(order_service):
    service, repo = order_service
    items = [{"nome": "p1", "p": 100, "q": 2, "tipo": "normal"}]
    order_id = service.create_order("Cliente", items, "normal")
    order = repo.get_by_id(order_id)
    # 100 * 2 = 200, sem desconto adicional
    assert order is not None
    assert order.total == pytest.approx(200.0)


def test_desconto_volume_acumulativo_com_desconto_item(order_service):
    service, repo = order_service
    items = [{"nome": "p1", "p": 100, "q": 3, "tipo": "desc10"}]
    order_id = service.create_order("Cliente", items, "normal")
    order = repo.get_by_id(order_id)
    # 100 * 3 * 0.9 = 270, com 15% volume off = 229.5
    assert order is not None
    assert order.total == pytest.approx(229.5)


def test_desconto_volume_com_4_unidades(order_service):
    service, repo = order_service
    items = [{"nome": "p1", "p": 50, "q": 4, "tipo": "normal"}]
    order_id = service.create_order("Cliente", items, "normal")
    order = repo.get_by_id(order_id)
    # 50 * 4 = 200, com 15% off = 170
    assert order is not None
    assert order.total == pytest.approx(170.0)


def test_desconto_volume_golden_master_nao_afetado(tmp_path, monkeypatch):
    """Sem VolumeDiscountCalculator, comportamento original e preservado."""
    monkeypatch.chdir(tmp_path)
    from legacy import Sis
    s = Sis()
    items = [{"nome": "produto1", "p": 100, "q": 3, "tipo": "normal"}]
    order_id = s.add_ped("Cliente", items, "normal")
    pedido = s.get_ped(order_id)
    # comportamento legado: sem desconto por volume
    assert pedido is not None
    assert pedido["tot"] == pytest.approx(300.0)
    s.close()
