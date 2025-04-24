from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import medicine  # noqa: F401
    import inventory  # noqa: F401
    import sales


class Cart:
    def __init__(self, sales_obj: sales.Sales, inventory_obj: inventory.Inventory):
        if sales_obj is None or inventory_obj is None:
            raise ValueError("Sales and Inventory objects cannot be None.")

        self.cart = {}
        self.sales = sales_obj
        self.inventory = inventory_obj

    def add_item(self, medicine_obj: medicine.Medicine, quantity: int):
        if medicine_obj is None:
            raise ValueError("Medicine cannot be None or not of type Medicine.")
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0.")
        if medicine_obj in self.cart:
            self.cart[medicine_obj] += quantity
        else:
            self.cart[medicine_obj] = quantity

    def remove_item(self, medicine_obj: medicine.Medicine, quantity: int):
        if medicine_obj is None:
            raise ValueError("Medicine cannot be None or not of type Medicine.")
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0.")
        if medicine_obj in self.cart:
            if self.cart[medicine_obj] >= quantity:
                self.cart[medicine_obj] -= quantity
                if self.cart[medicine_obj] == 0:
                    del self.cart[medicine_obj]
            else:
                raise ValueError("Not enough quantity to remove.")
        else:
            raise ValueError("Medicine not found in cart.")

    def calculate_total(self) -> float:
        total = 0.0
        item: medicine.Medicine
        quantity: int
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
                    "price": item.price,
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
