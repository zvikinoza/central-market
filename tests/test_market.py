from src.cashier import Cashier, BasicCashier
from src.manager import BasicManager, Manager
from src.payment import CashPaymentMethod, CreditCardPaymentMethod
from src.product import Item, Pack
from src.receipt import Receipt


def test_item() -> None:
    item1: Item = Item("Test1", 1.0)
    assert item1.name() == "Test1"
    assert item1.price() == 1.0


def test_cashier_reporting() -> None:
    manager: Manager = BasicManager()
    cashier: Cashier = BasicCashier(manager)
    manager.register_cashier(cashier)
    pack1: Pack = Pack([Item("Milk", 7.0), Item("Honey", 3.0)], 0.3)
    pack2: Pack = Pack([Item("Test3", 13.0), pack1], 0.3)
    receipt: Receipt = cashier.open_receipt([pack2])
    assert receipt.total_price() == 14.0
    # pass payment method that always is successful
    assert cashier.process_payment(receipt, CashPaymentMethod())
    # payment should be successful
    check, total_takings = cashier.get_report()
    print('\nReceipt: ', *check, f'Sum: {"{0:.2f}".format(total_takings)}', sep='\n')


def test_simulation() -> None:
    # market: Market = RandomMarketCreator().create_market()
    # client: Client = RandomClient()
    # products: list[Product] = market.get_product_list()
    # cashier: Cashier = market.get_free_cashier()
    # for _ in range(350):
    #     receipt: Receipt = cashier.open_receipt(client.choose_products(products))
    #     cashier.process_payment(receipt, client.get_payment_method())
    pass


def test_pack() -> None:
    pack: Pack = Pack([Item("Milk", 1.0), Item("Honey", 2.0)], 0.3)
    assert pack.name() == "Milk & Honey"
    assert pack.price() == 3.0 * 0.7


def test_nested_pack() -> None:
    pack1: Pack = Pack([Item("Milk", 7.0), Item("Honey", 3.0)], 0.3)
    pack2: Pack = Pack([Item("Test3", 13.0), pack1], 0.3)
    assert pack2.price() == 14.0
    assert pack2.name() == "Test3 & Milk & Honey"


def test_receipt() -> None:
    pack1: Pack = Pack([Item("Milk", 7.0), Item("Honey", 3.0)], 0.3)
    pack2: Pack = Pack([Item("Test3", 13.0), pack1], 0.3)
    receipt: Receipt = Receipt([pack1, pack2])
    assert receipt.total_price() == 21.0


def test_dummy_payment() -> None:
    amount = 17.0
    assert CashPaymentMethod().pay(amount) == amount
    assert CreditCardPaymentMethod().pay(amount) == amount


def test_cashier() -> None:
    cashier: Cashier = BasicCashier(BasicManager())
    pack1: Pack = Pack([Item("Milk", 7.0), Item("Honey", 3.0)], 0.3)
    pack2: Pack = Pack([Item("Test3", 13.0), pack1], 0.3)
    assert cashier.open_receipt([pack2]).total_price() == 14.0
