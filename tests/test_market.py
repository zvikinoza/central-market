from src.main import Market, RandomMarketCreator, Client, Product, Cashier, Receipt


def test_simulation() -> None:
    market: Market = RandomMarketCreator().create_market()
    client: Client = Client()
    products: list[Product] = market.get_product_list()
    cashier: Cashier = market.get_free_cashier()
    receipt: Receipt = cashier.open_receipt(client.choose_products(products))
    cashier.process_payment(receipt, client.get_payment_method())
