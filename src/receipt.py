from src.product import Product


class Receipt:
    def __init__(self, products: list[Product]):
        self.__products = products

    def total_price(self) -> float:
        total_price = sum(product.price() for product in self.__products)
        return total_price

    def __str__(self) -> str:
        return '\n'.join(f'{product.name()} {product.price()}' for product in self.__products)
