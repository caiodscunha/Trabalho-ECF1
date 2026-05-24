from src.interfaces.discount_strategy import IClientDiscountStrategy, IItemPriceCalculator
from src.interfaces.inventory import IInventoryProvider
from src.interfaces.notifier import INotifier
from src.interfaces.order_repository import IOrderRepository

__all__ = [
    "IClientDiscountStrategy",
    "IInventoryProvider",
    "IItemPriceCalculator",
    "INotifier",
    "IOrderRepository",
]
