from src.interfaces.discount_strategy import IClientDiscountStrategy, IItemPriceCalculator
from src.interfaces.inventory import IInventoryProvider
from src.interfaces.notifier import INotifier
from src.interfaces.order_event_observer import IOrderEventObserver
from src.interfaces.order_factory import IOrderFactory
from src.interfaces.order_repository import IOrderRepository
from src.interfaces.payment_strategy import IPaymentStrategy

__all__ = [
    "IClientDiscountStrategy",
    "IInventoryProvider",
    "IItemPriceCalculator",
    "INotifier",
    "IOrderEventObserver",
    "IOrderFactory",
    "IOrderRepository",
    "IPaymentStrategy",
]