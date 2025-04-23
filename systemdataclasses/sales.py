from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import medicine  # noqa: F401
    import inventory  # noqa: F401
    import cart  # noqa: F401


class Sales:
    def __init__(self):
        self.sales_list = []

    def add_sale(self, cart_obj: cart.Cart):
        self.sales_list.append(cart_obj)

    def get_sales_statistics(self):
        quantity_data = {}
        value_data = {}
        mapping = {}

        cart: cart.Cart
        for cart in self.sales_list:
            for medicine_obj, quantity in cart.get_cart().items():
                if medicine_obj.identifier not in mapping:
                    mapping.update({medicine_obj.identifier: medicine_obj})
                if medicine_obj.identifier not in quantity_data:
                    quantity_data.update({medicine_obj.identifier: 0})
                    value_data.update({medicine_obj.identifier: 0})
                quantity_data[medicine_obj.identifier] += quantity
                value_data[medicine_obj.identifier] += medicine_obj.price * quantity

        result = []
        for identifier in mapping:
            medicine_data = mapping[identifier].toJson()
            medicine_data["quantity_sold"] = quantity_data[identifier]
            medicine_data["value_sold"] = value_data[identifier]
            result.append(medicine_data)

        return result

    def get_sales_history_json(self) -> list[cart.Cart]:
        res = []
        cart_obj: cart.Cart
        for cart_obj in self.sales_list:
            res.append(cart_obj.get_cart_json())
        return res
