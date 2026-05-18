from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Order:
    """Entidade de domínio: representa um pedido.

    Modelo anêmico por intenção nesta sprint: a regra de cálculo de total e
    as transições de estado vivem em ``services`` (SRP), e a persistência
    vive em ``repositories``. Aqui ficam apenas os dados.
    """

    cliente: str
    itens: list[dict[str, Any]]
    total: float
    status: str
    data: str
    tipo_cliente: str
    id: Optional[int] = None
