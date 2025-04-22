from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import medicine  # noqa: F401
    import inventory  # noqa: F401
    import sales


class Cart:
    def __init__(self, sales: sales.Sales):
        self.cart = {}
        self.sales = sales

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
    
    def generate_receipt(self) -> str:
        self.sales.add_sale(self)
        receipt = "Receipt:\n"
        for item, quantity in self.cart.items():
            receipt += f"{item.name} (x{quantity}): ${item.price * quantity:.2f}\n"
        receipt += f"Total: ${self.calculate_total():.2f}"
        return receipt
    
    def get_cart(self) -> dict[medicine.Medicine, int]:
        return self.cart
