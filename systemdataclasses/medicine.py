from __future__ import annotations
from typing import TYPE_CHECKING
import time

if TYPE_CHECKING:
    import vendor  # noqa: F401
    import batch


class Medicine:
    def __init__(
        self,
        name: str,
        batch: batch.Batch,
        expiry_date: str,
        price: float,
        vendor: vendor.Vendor,
    ):
        self.name = name
        self.identifier = name.replace(" ", "_").lower() + "_" + str(time.time())
        self.batch = batch
        self.expiry_date = expiry_date
        self.price = price
        self.vendor = vendor

    def __str__(self):
        return f"Medicine(name={self.name}, batch_number={str(self.batch)}, expiry_date={self.expiry_date}, price={self.price}, vendor={self.vendor})"

    def toJson(self):
        return {
            "name": self.name,
            "identifier": self.identifier,
            "batch": self.batch.toJson(),
            "expiry_date": self.expiry_date,
            "price": self.price,
            "vendor": self.vendor.toJson(),
        }


class MedicineList:
    def __init__(self):
        self.medicines = []

    def add_medicine(self, medicine: Medicine):
        self.medicines.append(medicine)

    def remove_medicine(self, identifier: str):
        self.medicines = [
            medicine for medicine in self.medicines if medicine.identifier != identifier
        ]

    def find_medicine(self, identifier: str):
        for medicine in self.medicines:
            if medicine.identifier == identifier:
                return medicine
        return None
    
    def get_medicines(self):
        return self.medicines

    def toJson(self):
        return [medicine.toJson() for medicine in self.medicines]
