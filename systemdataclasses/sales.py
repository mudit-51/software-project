from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import medicine  # noqa: F401
    import inventory  # noqa: F401
    import cart  # noqa: F401


class Sales:
    def __init__(self):
        self.sales_list = []

    def add_sale(self, cart):
        if isinstance(cart, cart.Cart):
            self.sales_list.append(cart)
        else:
            raise ValueError("Invalid cart object.")

    def rank_by_quantity(self) -> list[medicine.Medicine]:
        ranked = {}

        cart: cart.Cart
        for cart in self.sales_list:
            for medicine, quantity in cart.get_cart().items():
                ranked[medicine] += quantity
        ranked_sales = sorted(ranked.items(), key=lambda x: x[1], reverse=True)
        ranked_sales = [item[0] for item in ranked_sales]
        return ranked_sales

    def rank_by_value(self) -> list[medicine.Medicine]:
        ranked = {}

        cart: cart.Cart
        for cart in self.sales_list:
            for medicine, quantity in cart.get_cart().items():
                ranked[medicine] += medicine.price * quantity
        ranked_sales = sorted(ranked.items(), key=lambda x: x[1], reverse=True)
        ranked_sales = [item[0] for item in ranked_sales]
        return ranked_sales
    
    def get_sales_history(self) -> list[cart.Cart]:
        return self.sales_list
