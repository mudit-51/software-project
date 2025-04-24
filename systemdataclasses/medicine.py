from __future__ import annotations
from datetime import datetime
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
        if batch is None:
            raise ValueError("Batch cannot be None")
        if vendor is None:
            raise ValueError("Vendor cannot be None")
        if name is None or name == "":
            raise ValueError("Name cannot be None or empty")
        if expiry_date is None or expiry_date == "":
            raise ValueError("Expiry date cannot be None or empty")
        if price <= 0:
            raise ValueError("Price must be greater than 0")
        try:
            datetime.strptime(expiry_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Expiry date must be in YYYY-MM-DD format")
        self.name = name
        self.identifier = name.replace(" ", "_").lower() + "_" + str(time.time())
        self.batch = batch
        self.expiry_date = expiry_date
        self.price = price
        self.vendor = vendor

    def send_to_vendor(self, quantity: int):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        obj = self.toJson()
        obj["quantity"] = quantity
        self.vendor.add_order(obj)

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

    def add_medicine(self, medicine_obj: Medicine):
        if medicine_obj is None:
            raise ValueError("Medicine cannot be None or not of type Medicine")
        self.medicines.append(medicine_obj)

    def remove_medicine(self, identifier: str):
        self.medicines = [
            medicine_obj
            for medicine_obj in self.medicines
            if medicine_obj.identifier != identifier
        ]

    def find_medicine(self, identifier: str):
        for medicine_obj in self.medicines:
            if medicine_obj.identifier == identifier:
                return medicine_obj
        return None

    def get_medicines(self):
        return self.medicines

    def toJson(self):
        return [medicine_obj.toJson() for medicine_obj in self.medicines]
