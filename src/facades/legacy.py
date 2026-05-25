from typing import Any, Optional

from src.factories.order_factory import SpecialOrderFactory, StandardOrderFactory
from src.models.order import Order
from src.repositories.sqlite_order_repository import SqliteOrderRepository
from src.services.inventory_service import (
    InventoryService,
    StaticInventoryProvider,
)
from src.observers.notification_observer import (
    AccountManagerOrderObserver,
    EmailOrderObserver,
    PointsOrderObserver,
    SmsOrderObserver,
)
from src.services.notification_service import ConsoleNotifier, NotificationService
from src.services.order_service import OrderService
from src.services.payment_service import PaymentService
from src.services.report_service import ReportService


class Sis:
    """Facade compatível com a API legada do sistema de pedidos."""

    def __init__(self) -> None:
        self._repository = SqliteOrderRepository("loja.db")
        notifier = ConsoleNotifier()
        notifications = NotificationService()
        notifications.subscribe(EmailOrderObserver(notifier))
        notifications.subscribe(SmsOrderObserver(notifier))
        notifications.subscribe(AccountManagerOrderObserver(notifier))
        notifications.subscribe(PointsOrderObserver())
        self._order_service = OrderService(self._repository, notifications)
        self._factory = StandardOrderFactory(self._order_service)
        self._payment_service = PaymentService(self._repository, notifications)
        self._inventory_service = InventoryService(StaticInventoryProvider())
        self._report_service = ReportService(self._repository)

    def add_ped(self, n: str, its: list[dict[str, Any]], t: str) -> int:
        return self._factory.create(n, its, t)

    def get_ped(self, id: int) -> Optional[dict[str, Any]]:
        order = self._repository.get_by_id(id)
        if order is None:
            return None
        return _order_to_legacy_dict(order)

    def upd_st(self, id: int, s: str) -> None:
        self._order_service.update_status(id, s)

    def calc_tot_cli(self, n: str) -> float:
        return self._order_service.total_for_client(n)

    def gerar_rel(self, tipo: str) -> None:
        if tipo == "vendas":
            self._report_service.sales_report()
        elif tipo == "clientes":
            self._report_service.clients_report()

    def proc_pag(self, id: int, m: str, vl: float) -> bool:
        return self._payment_service.process_payment(id, m, vl)

    def validar_estoque(self, its: list[dict[str, Any]]) -> bool:
        return self._inventory_service.validate(its)

    def cancelar_pedido(self, id: int) -> None:
        self._order_service.cancel_order(id)

    def close(self) -> None:
        self._repository.close()


class PedEspecial:
    """Fachada legada para pedidos especiais via composição (não herança).

    LSP: remove a violação onde PedEspecial estendia Sis e sobrescrevia métodos
    quebrando contratos (upd_st ignorava notificações, add_ped aplicava taxa
    dentro do loop acumulativo). Agora usa SpecialOrderFactory por composição.
    """

    def __init__(self) -> None:
        self._repository = SqliteOrderRepository("loja.db")
        self._factory = SpecialOrderFactory(self._repository)

    def add_ped(self, n: str, its: list[dict[str, Any]], t: str) -> int:
        return self._factory.create(n, its, t)

    def get_ped(self, id: int) -> Optional[dict[str, Any]]:
        order = self._repository.get_by_id(id)
        if order is None:
            return None
        return _order_to_legacy_dict(order)

    def upd_st(self, id: int, s: str) -> None:
        order = self._repository.get_by_id(id)
        if order is None:
            return
        self._repository.update_status(id, s)
        print(f"Pedido especial {id} -> {s}")

    def close(self) -> None:
        self._repository.close()


def _order_to_legacy_dict(order: Order) -> dict[str, Any]:
    return {
        "id": order.id,
        "cli": order.cliente,
        "itens": order.itens,
        "tot": order.total,
        "st": order.status,
        "dt": order.data,
        "tp": order.tipo_cliente,
    }


def main() -> None:
    s = Sis()
    its1 = [
        {"nome": "produto1", "p": 100, "q": 2, "tipo": "normal"},
        {"nome": "produto2", "p": 50, "q": 1, "tipo": "desc10"},
    ]
    if s.validar_estoque(its1):
        id1 = s.add_ped("Joao Silva", its1, "normal")
        print(f"Pedido {id1} criado!")
        s.proc_pag(id1, "cartao", 250)
        s.upd_st(id1, "enviado")
        s.upd_st(id1, "entregue")

    its2 = [{"nome": "produto3", "p": 200, "q": 1, "tipo": "desc20"}]
    if s.validar_estoque(its2):
        id2 = s.add_ped("Maria Santos", its2, "vip")
        s.proc_pag(id2, "pix", 160)

    its3 = [{"nome": "produto1", "p": 100, "q": 5, "tipo": "normal"}]
    if s.validar_estoque(its3):
        id3 = s.add_ped("Empresa XYZ", its3, "corporativo")
        s.proc_pag(id3, "boleto", 500)

    s.gerar_rel("vendas")
    print()
    s.gerar_rel("clientes")
    s.close()


if __name__ == "__main__":
    main()
