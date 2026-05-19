from src.interfaces.order_repository import IOrderRepository


class ReportService:
    """Gera os relatórios de vendas e clientes a partir do repository."""

    def __init__(self, repository: IOrderRepository) -> None:
        self._repository = repository

    def sales_report(self) -> None:
        orders = self._repository.list_all()
        print("=== RELATORIO DE VENDAS ===")
        total_geral: float = 0
        for order in orders:
            print(
                f"Pedido #{order.id} - Cliente: {order.cliente} - "
                f"Total: R${order.total:.2f} - Status: {order.status}"
            )
            total_geral += order.total
        print(f"Total Geral: R${total_geral:.2f}")
        with open("rel_vendas.txt", "w") as f:
            f.write(f"Total de vendas: {total_geral}")

    def clients_report(self) -> None:
        clients = self._repository.list_distinct_clients()
        print("=== RELATORIO DE CLIENTES ===")
        for client, client_type in clients:
            total = self._repository.sum_total_by_client(client)
            print(
                f"Cliente: {client} ({client_type}) - "
                f"Total gasto: R${total:.2f}"
            )
        with open("rel_clientes.txt", "w") as f:
            for client, client_type in clients:
                f.write(f"{client},{client_type}\n")
