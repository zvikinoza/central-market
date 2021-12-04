from src.product import Product


class Receipt:
    __products: list[Product]

    def __init__(self, products: list[Product]):
        self.__products = products

    def total_price(self) -> float:
        total_price = sum(product.price() for product in self.__products)
        return total_price

    def __str__(self) -> str:
        return ''.join(f'product=[{str(product)}]\n' for product in self.__products)

    def __repr__(self) -> str:
        return str(self)
