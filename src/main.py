from src.cashier import Cashier
from src.client import Client, RandomClient
from src.market import Market, RandomMarketCreator
from src.product import Product
from src.receipt import Receipt


def test_simulation() -> None:
    market: Market = RandomMarketCreator().create_market()
    client: Client = RandomClient()
    products: list[Product] = market.get_product_list()
    cashier: Cashier = market.get_free_cashier()
    for _ in range(30):
        receipt: Receipt = cashier.open_receipt(client.choose_products(products))
        cashier.process_payment(receipt, client.get_payment_method())


if __name__ == '__main__':
    test_simulation()
