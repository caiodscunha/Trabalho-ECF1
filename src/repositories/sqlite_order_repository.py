import json
import sqlite3
from typing import Optional

from src.interfaces.order_repository import IOrderRepository
from src.models.order import Order


class SqliteOrderRepository(IOrderRepository):
    """Implementação concreta do IOrderRepository usando SQLite.

    Toda referência a SQL e à biblioteca sqlite3 fica contida nesta classe.
    Os serviços enxergam apenas o contrato IOrderRepository.
    """

    def __init__(self, db_path: str = "loja.db") -> None:
        self._connection = sqlite3.connect(db_path)
        self._cursor = self._connection.cursor()
        self._create_schema()

    def _create_schema(self) -> None:
        self._cursor.execute(
            """CREATE TABLE IF NOT EXISTS ped (
                id INTEGER PRIMARY KEY, cli TEXT, itens TEXT,
                tot REAL, st TEXT, dt TEXT, tp TEXT)"""
        )
        self._connection.commit()

    def add(self, order: Order) -> int:
        items_json = json.dumps(order.itens)
        self._cursor.execute(
            "INSERT INTO ped (cli, itens, tot, st, dt, tp) VALUES (?, ?, ?, ?, ?, ?)",
            (
                order.cliente,
                items_json,
                order.total,
                order.status,
                order.data,
                order.tipo_cliente,
            ),
        )
        self._connection.commit()
        return int(self._cursor.lastrowid or 0)

    def get_by_id(self, order_id: int) -> Optional[Order]:
        self._cursor.execute("SELECT * FROM ped WHERE id=?", (order_id,))
        row = self._cursor.fetchone()
        if row is None:
            return None
        return self._row_to_order(row)

    def update_status(self, order_id: int, status: str) -> None:
        self._cursor.execute("UPDATE ped SET st=? WHERE id=?", (status, order_id))
        self._connection.commit()

    def list_all(self) -> list[Order]:
        self._cursor.execute("SELECT * FROM ped")
        return [self._row_to_order(r) for r in self._cursor.fetchall()]

    def list_distinct_clients(self) -> list[tuple[str, str]]:
        self._cursor.execute("SELECT DISTINCT cli, tp FROM ped")
        return [(r[0], r[1]) for r in self._cursor.fetchall()]

    def sum_total_by_client(self, client: str) -> float:
        self._cursor.execute("SELECT * FROM ped WHERE cli=?", (client,))
        return sum(r[3] for r in self._cursor.fetchall())

    def close(self) -> None:
        self._connection.close()

    @staticmethod
    def _row_to_order(row: tuple) -> Order:
        return Order(
            id=row[0],
            cliente=row[1],
            itens=json.loads(row[2]),
            total=row[3],
            status=row[4],
            data=row[5],
            tipo_cliente=row[6],
        )
