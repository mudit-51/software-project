from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import medicine  # noqa: F401
    import inventory  # noqa: F401
    import sales


class Cart:
    def __init__(self, sales: sales.Sales, inventory: inventory.Inventory):
        self.cart = {}
        self.sales = sales
        self.inventory = inventory

    def add_item(self, medicine: medicine.Medicine, quantity: int):
        if medicine in self.cart:
            self.cart[medicine] += quantity
        else:
            self.cart[medicine] = quantity

    def remove_item(self, medicine: medicine.Medicine, quantity: int):
        if medicine in self.cart:
            if self.cart[medicine] >= quantity:
                self.cart[medicine] -= quantity
                if self.cart[medicine] == 0:
                    del self.cart[medicine]
            else:
                raise ValueError("Not enough quantity to remove.")
        else:
            raise ValueError("Medicine not found in cart.")

    def calculate_total(self) -> float:
        total = 0.0
        for item, quantity in self.cart.items():
            total += item.price * quantity
        return total

    def generate_reciept_json(self):
        receipt = {"items": [], "total": self.calculate_total()}
        item: medicine.Medicine
        for item, quantity in self.cart.items():
            if self.inventory.get_quantity(item) < quantity:
                raise ValueError(f"Not enough {item.name} in inventory.")
            self.inventory.remove_medicine(item, quantity)
            receipt["items"].append(
                {
                    "name": item.name,
                    "quantity": quantity,
                    "price": item.price * quantity,
                }
            )
        self.sales.add_sale(self)
        return receipt

    def get_cart(self) -> dict[medicine.Medicine, int]:
        return self.cart
    
    
    def get_cart_json(self):
        res = []
        for item, quantity in self.cart.items():
            item_json = item.toJson()
            item_json["quantity"] = quantity
            item_json["total_price"] = item.price * quantity
            res.append(item_json)
        return res
