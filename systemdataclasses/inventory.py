from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import medicine


class Inventory:
    def __init__(
        self, medicines: list[medicine.Medicine] = None, quantity: list[int] = None
    ):
        if medicines is None or quantity is None:
            self.inventory = {}
            return
        if len(medicines) != len(quantity):
            raise ValueError("Medicines and quantities must have the same length.")
        self.inventory = {}
        for med, qty in zip(medicines, quantity):
            self.inventory[med] = qty

    def queue_order(self, medicine: medicine.Medicine, quantity: int):
        medicine.send_to_vendor(quantity)

    def add_medicine(self, medicine: medicine.Medicine, quantity: int):
        if medicine in self.inventory:
            self.inventory[medicine] += quantity
        else:
            self.inventory[medicine] = quantity

    def remove_medicine(self, medicine: medicine.Medicine, quantity: int):
        if medicine in self.inventory:
            if self.inventory[medicine] >= quantity:
                self.inventory[medicine] -= quantity
                if self.inventory[medicine] == 0:
                    del self.inventory[medicine]
            else:
                raise ValueError("Not enough quantity to remove.")
        else:
            raise ValueError("Medicine not found in inventory.")

    def get_quantity(self, medicine: medicine.Medicine) -> int:
        return self.inventory.get(medicine, 0)

    def search_medicine(self, id: str) -> medicine.Medicine:
        for med in self.inventory.keys():
            if med.identifier == id:
                return med
        raise ValueError("Medicine not found in inventory.")

    def get_medicines(self) -> list[medicine.Medicine]:
        return list(self.inventory.keys())

    def get_stock_valuation(self) -> float:
        total_value = 0.0

        med: medicine.Medicine
        qty: int
        for med, qty in self.inventory.items():
            total_value += med.price * qty
        return total_value

    def get_threshold_alerts(
        self, threshold: int
    ) -> list[tuple[medicine.Medicine, int]]:
        alerts = []
        for med, qty in self.inventory.items():
            if qty <= threshold:
                alerts.append((med, qty))
        return alerts

    def track_batch_expiry(
        self, current_date: str
    ) -> list[tuple[medicine.Medicine, str]]:
        expired_medicines = []
        for med in self.inventory.keys():
            if med.batch.expiry_date < current_date:
                expired_medicines.append((med, med.batch.expiry_date))
        return expired_medicines

    def __str__(self):
        return f"Inventory(medicine={self.medicine}, quantity={self.quantity})"

    def toJson(self):
        return [
            {
                "medicine": med.toJson(),
                "quantity": qty,
            }
            for med, qty in self.inventory.items()
        ]

    def threshold_toJson(self, threshold: int):
        return [
            {
                "medicine": med.toJson(),
                "quantity": qty,
            }
            for med, qty in self.inventory.items()
            if qty <= threshold
        ]

    def expiry_toJson(self, current_date: str):
        return [
            {
                "medicine": med.toJson(),
                "expiry_date": med.batch.expiry_date,
                "quantity": qty,
            }
            for med, qty in self.inventory.items()
            if med.batch.expiry_date < current_date
        ]
